from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.hooks.postgres_hook import PostgresHook
from datetime import timedelta
import requests


def fetch_bitcoin_price(**kwargs):
    api_url = Variable.get("bitcoin_price_pipeline_api_url")
    response = requests.get(api_url)
    response.raise_for_status()
    kwargs['ti'].xcom_push(key='raw_data', value=response.json())

def parse_bitcoin_data(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(key='raw_data')
    time_updated = raw_data["time"]["updatedISO"]
    rates = {
        "USD": raw_data["bpi"]["USD"]["rate_float"],
        "GBP": raw_data["bpi"]["GBP"]["rate_float"],
        "EUR": raw_data["bpi"]["EUR"]["rate_float"]
    }
    
    kwargs['ti'].xcom_push(key='parsed_data', value={"time_updated": time_updated, "rates": rates})

def save_to_postgres(**kwargs):
    parsed_data = kwargs['ti'].xcom_pull(key='parsed_data')
    time_updated = parsed_data["time_updated"]
    rates = parsed_data["rates"]
    
    pg_hook = PostgresHook(postgres_conn_id="bitcoin_price_pipeline_database")
    insert_query = """
        INSERT INTO bitcoin_prices (timestamp, usd_rate, gbp_rate, eur_rate)
        VALUES (%s, %s, %s, %s)
    """
    pg_hook.run(insert_query, parameters=(time_updated, rates["USD"], rates["GBP"], rates["EUR"]))

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="bitcoin_price_pipeline",
    default_args=default_args,
    description="Fetches and stores Bitcoin price in PostgreSQL",
    schedule_interval=timedelta(hours=1),
    start_date=days_ago(1),
    catchup=False
) as dag:

    fetch_data = PythonOperator(
        task_id="fetch_bitcoin_price",
        python_callable=fetch_bitcoin_price,
        provide_context=True
    )

    parse_data = PythonOperator(
        task_id="parse_bitcoin_data",
        python_callable=parse_bitcoin_data,
        provide_context=True
    )

    save_data = PythonOperator(
        task_id="save_to_postgres",
        python_callable=save_to_postgres,
        provide_context=True
    )

    fetch_data >> parse_data >> save_data