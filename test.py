cat << 'EXIT' > ~/airflow_project/dags/incremental_stored_proc.py
import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

def execute_incremental_loop(iterations=6, interval_seconds=10):
    hook = PostgresHook(postgres_conn_id="my_target_db")
    conn = hook.get_conn()
    cursor = conn.cursor()
    try:
        for i in range(1, iterations + 1):
            cursor.execute("CALL public.process_incremental_records();")
            conn.commit()
            print(f"Cycle {i}/{iterations}: incremental stored procedure executed.")
            time.sleep(interval_seconds)
    finally:
        cursor.close()
        conn.close()

with DAG(
    dag_id="incremental_stored_proc_10s",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
) as dag:

    run_proc_task = PythonOperator(
        task_id="run_proc_loop_task",
        python_callable=execute_incremental_loop,
        op_kwargs={"iterations": 6, "interval_seconds": 10},
    )
EXIT