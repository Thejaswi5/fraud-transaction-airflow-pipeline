from pathlib import Path

from config.settings import REQUIRED_COLUMNS
from src.fraud_rules import create_fraud_risk_flags
from src.ingestion import ingest_transactions


def test_create_fraud_risk_flags_writes_expected_counts(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    processed_file = tmp_path / "daily_transactions.csv"
    flagged_file = tmp_path / "flagged_transactions.csv"

    ingest_transactions(
        source_file=source_file,
        output_file=processed_file,
        selected_columns=REQUIRED_COLUMNS,
    )

    result = create_fraud_risk_flags(
        input_file=processed_file,
        output_file=flagged_file,
        high_amount_threshold=1000.0,
    )

    assert result["rows_written"] == 3
    assert result["high_amount_count"] == 1
    assert result["labeled_fraud_count"] == 1
    assert result["credit_card_count"] == 1


def test_create_fraud_risk_flags_adds_expected_columns(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    processed_file = tmp_path / "daily_transactions.csv"
    flagged_file = tmp_path / "flagged_transactions.csv"

    ingest_transactions(
        source_file=source_file,
        output_file=processed_file,
        selected_columns=REQUIRED_COLUMNS,
    )

    create_fraud_risk_flags(
        input_file=processed_file,
        output_file=flagged_file,
        high_amount_threshold=1000.0,
    )

    header = flagged_file.read_text(encoding="utf-8").splitlines()[0]

    assert "high_transaction_amount" in header
    assert "labeled_fraud" in header
    assert "missing_payer_email_domain" in header
    assert "credit_card_transaction" in header
