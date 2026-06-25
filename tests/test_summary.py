from pathlib import Path

from config.settings import REQUIRED_COLUMNS
from src.fraud_rules import create_fraud_risk_flags
from src.ingestion import ingest_transactions
from src.summary import build_daily_fraud_summary


def test_build_daily_fraud_summary_returns_expected_metrics(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    processed_file = tmp_path / "daily_transactions.csv"
    flagged_file = tmp_path / "flagged_transactions.csv"
    summary_file = tmp_path / "daily_fraud_summary.csv"

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

    result = build_daily_fraud_summary(
        input_file=flagged_file,
        output_file=summary_file,
    )

    assert result["total_transactions"] == 3
    assert result["fraud_transactions"] == 1
    assert result["fraud_rate"] == 0.3333
    assert result["high_amount_transactions"] == 1
    assert result["credit_card_transactions"] == 1
    assert result["total_transaction_amount"] == 1384.24


def test_build_daily_fraud_summary_writes_output_file(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    processed_file = tmp_path / "daily_transactions.csv"
    flagged_file = tmp_path / "flagged_transactions.csv"
    summary_file = tmp_path / "daily_fraud_summary.csv"

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

    build_daily_fraud_summary(
        input_file=flagged_file,
        output_file=summary_file,
    )

    output_lines = summary_file.read_text(encoding="utf-8").strip().splitlines()

    assert summary_file.exists()
    assert len(output_lines) == 2
    assert "total_transactions" in output_lines[0]
