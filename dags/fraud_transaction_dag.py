from datetime import datetime, timedelta
import sys
from pathlib import Path

from airflow.decorators import dag, task

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.settings import (
    FRAUD_SUMMARY_FILE,
    MIN_EXPECTED_ROWS,
    PROCESSED_DATA_DIR,
    PROCESSED_TRANSACTION_FILE,
    RAW_TRANSACTION_FILE,
    REQUIRED_COLUMNS,
)
from src.fraud_rules import create_fraud_risk_flags
from src.ingestion import ingest_transactions
from src.reconciliation import reconcile_row_counts
from src.summary import build_daily_fraud_summary
from src.validation import validate_source_file


def on_task_failure(context):
    task_instance = context.get("task_instance")
    exception = context.get("exception")

    dag_id = task_instance.dag_id if task_instance else "unknown_dag"
    task_id = task_instance.task_id if task_instance else "unknown_task"

    print(
        f"ALERT: Airflow task failed. "
        f"dag_id={dag_id}, task_id={task_id}, error={exception}"
    )


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": on_task_failure,
}


@dag(
    dag_id="fraud_transaction_pipeline",
    description="Validate, ingest, reconcile, flag, and summarize fraud transaction data.",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["fraud", "transactions", "batch"],
)
def fraud_transaction_pipeline():
    @task
    def validate_source():
        return validate_source_file(
            RAW_TRANSACTION_FILE,
            REQUIRED_COLUMNS,
            MIN_EXPECTED_ROWS,
        )

    @task
    def ingest_transactions_task(_validation_result: dict):
        return ingest_transactions(
            source_file=RAW_TRANSACTION_FILE,
            output_file=PROCESSED_TRANSACTION_FILE,
            selected_columns=REQUIRED_COLUMNS,
        )

    @task
    def reconcile_counts(_ingestion_result: dict):
        return reconcile_row_counts(
            source_file=RAW_TRANSACTION_FILE,
            target_file=PROCESSED_TRANSACTION_FILE,
        )

    @task
    def create_flags(_reconciliation_result: dict):
        return create_fraud_risk_flags(
            input_file=PROCESSED_TRANSACTION_FILE,
            output_file=PROCESSED_DATA_DIR / "flagged_transactions.csv",
            high_amount_threshold=1000.0,
        )

    @task
    def build_summary(_flags_result: dict):
        return build_daily_fraud_summary(
            input_file=PROCESSED_DATA_DIR / "flagged_transactions.csv",
            output_file=FRAUD_SUMMARY_FILE,
        )

    @task
    def notify_success(summary_result: dict):
        print("Fraud transaction pipeline completed successfully.")
        print(summary_result)
        return summary_result

    validation_result = validate_source()
    ingestion_result = ingest_transactions_task(validation_result)
    reconciliation_result = reconcile_counts(ingestion_result)
    flags_result = create_flags(reconciliation_result)
    summary_result = build_summary(flags_result)
    notify_success(summary_result)


fraud_transaction_pipeline()
