import json
import requests

AIRFLOW_URL = "http://localhost:8080/api/v1"
AIRFLOW_VARIABLES_URL = f"{AIRFLOW_URL}/variables"
AIRFLOW_CONNECTIONS_URL = f"{AIRFLOW_URL}/connections"
AIRFLOW_API_TOKEN = "YWlyZmxvdzphaXJmbG93"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {AIRFLOW_API_TOKEN}"
}

config = {
    "variables": {
        "bitcoin_price_pipeline_api_url": "https://api.coindesk.com/v1/bpi/currentprice.json"
    },
    "connections": {
        "bitcoin_price_pipeline_database": {
            "host": "localhost",
            "login": "postgres",
            "password": "postgres",
            "schema": "bitcoin_data",
            "port": 5432,
            "conn_type": "postgres"
        }
    }
}

variables = config.get('variables', {})
connections = config.get('connections', {})


def update_variable(key, value):
    data = {
        "key": key,
        "value": value
    }

    response = requests.post(AIRFLOW_VARIABLES_URL,
                             headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"Variável {key} atualizada com sucesso.")
    elif response.status_code == 409:
        response = requests.patch(
            f"{AIRFLOW_VARIABLES_URL}/{key}", headers=headers, data=json.dumps(data))
    else:
        print(
            f"Falha ao atualizada variável {key}: {response.status_code}, {response.text}")


def update_connection(conn_id, conn_data):
    data = {
        "connection_id": conn_id,
        "conn_type": conn_data["conn_type"],
        "login": conn_data.get("login"),
        "password": conn_data.get("password"),
        "host": conn_data.get("host"),
        "schema": conn_data.get("schema"),
        "port": conn_data.get("port")
    }

    response = requests.post(AIRFLOW_CONNECTIONS_URL,
                             headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"Conexão {conn_id} atualizada com sucesso.")
    elif response.status_code == 409:
        response = requests.patch(
            f"{AIRFLOW_CONNECTIONS_URL}/{conn_id}", headers=headers, data=json.dumps(data))
    else:
        print(
            f"Falha ao atualizada conexão {conn_id}: {response.status_code}, {response.text}")


for key, value in variables.items():
    update_variable(key, value)

for conn_id, conn_data in connections.items():
    update_connection(conn_id, conn_data)
