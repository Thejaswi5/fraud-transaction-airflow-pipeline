# Fraud Transaction Airflow Pipeline

A production-style Apache Airflow project for orchestrating a fraud transaction analytics pipeline using real-world transaction data.

The project focuses on reliable batch orchestration: validating source files, ingesting transaction data, enforcing schema checks, reconciling row counts, creating fraud-risk flags, and producing daily fraud monitoring outputs.

## Problem Statement

Fraud operations teams rely on fresh, complete, and trustworthy transaction data. If an ingestion job fails silently, downstream reports may show stale metrics. If a partial file is loaded, analysts may investigate incorrect numbers. If schema changes are not detected early, transformation jobs may fail after bad data has already moved downstream.

This project demonstrates how an orchestrated pipeline can reduce those risks through task dependencies, validation gates, retries, logging, and backfill-ready processing.

## Dataset

This project is designed to work with the IEEE-CIS Fraud Detection transaction dataset.

Expected local file location:

```text
data/raw/train_transaction.csv
