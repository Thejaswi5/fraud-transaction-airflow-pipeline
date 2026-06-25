from pathlib import Path

import pytest

from config.settings import REQUIRED_COLUMNS
from src.ingestion import ingest_transactions
from src.reconciliation import count_csv_rows, reconcile_row_counts


def test_count_csv_rows_excludes_header():
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")

    assert count_csv_rows(source_file) == 3


def test_reconcile_row_counts_passes_when_counts_match(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    target_file = tmp_path / "daily_transactions.csv"

    ingest_transactions(
        source_file=source_file,
        output_file=target_file,
        selected_columns=REQUIRED_COLUMNS,
    )

    result = reconcile_row_counts(source_file, target_file)

    assert result["source_count"] == 3
    assert result["target_count"] == 3
    assert result["status"] == "matched"


def test_reconcile_row_counts_fails_when_counts_do_not_match(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    target_file = tmp_path / "daily_transactions.csv"

    target_file.write_text(
        "TransactionID,isFraud\n10001,0\n10002,1\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Row count mismatch"):
        reconcile_row_counts(source_file, target_file)
