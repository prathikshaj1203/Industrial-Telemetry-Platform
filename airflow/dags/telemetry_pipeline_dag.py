from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def telemetry_pipeline():
    print("Telemetry Pipeline Running...")
    print("Kafka → Validation → PostgreSQL pipeline active")

default_args = {
    'owner': 'prathiksha',
}

with DAG(
    dag_id='industrial_telemetry_pipeline',
    default_args=default_args,
    start_date=datetime(2026, 5, 12),
    schedule='*/1 * * * *',
    catchup=False,
) as dag:

    run_pipeline = PythonOperator(
        task_id='run_telemetry_pipeline',
        python_callable=telemetry_pipeline
    )

    run_pipeline