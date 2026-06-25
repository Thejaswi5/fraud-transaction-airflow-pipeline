# Fraud Transaction Airflow Pipeline

Batch data pipeline for validating and preparing transaction data for fraud analysis.

The project is being built in small pieces. The current focus is the local Python pipeline logic first. Airflow orchestration will be added after the validation, ingestion, reconciliation, and summary steps are working locally.

## Current status

Done:

- project folder structure
- Git ignore rules for raw data, processed data, logs, local databases, and virtual environments
- shared pipeline settings
- source file validation
- transaction ingestion
- sample test fixtures
- unit tests for validation logic

In progress:

- ingestion tests
- row-count reconciliation
- fraud flag rules
- daily fraud summary output
- Airflow DAG

## Dataset

The pipeline is designed for the IEEE-CIS fraud transaction dataset.

Expected local file path:

```text
data/raw/train_transaction.csv EOF
