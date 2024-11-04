FROM apache/airflow:2.9.3-python3.10

USER root

RUN apt-get update && apt-get install -y \
    python3-psycopg2 \
    postgresql \
    postgresql-contrib \
    gcc \
    build-essential \
    libpq-dev

COPY /bitcoin_price_pipeline /opt/airflow/dags/bitcoin_price_pipeline

USER airflow