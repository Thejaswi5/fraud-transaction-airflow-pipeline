from pathlib import Path

from config.settings import REQUIRED_COLUMNS
from src.ingestion import ingest_transactions


def test_ingest_transactions_writes_expected_rows(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    output_file = tmp_path / "daily_transactions.csv"

    result = ingest_transactions(
        source_file=source_file,
        output_file=output_file,
        selected_columns=REQUIRED_COLUMNS,
    )

    output_lines = output_file.read_text(encoding="utf-8").strip().splitlines()

    assert result["rows_written"] == 3
    assert result["columns_written"] == len(REQUIRED_COLUMNS)
    assert len(output_lines) == 4


def test_ingest_transactions_is_idempotent_for_same_input(tmp_path):
    source_file = Path("tests/fixtures/valid_transactions_sample.csv")
    output_file = tmp_path / "daily_transactions.csv"

    ingest_transactions(
        source_file=source_file,
        output_file=output_file,
        selected_columns=REQUIRED_COLUMNS,
    )

    ingest_transactions(
        source_file=source_file,
        output_file=output_file,
        selected_columns=REQUIRED_COLUMNS,
    )

    output_lines = output_file.read_text(encoding="utf-8").strip().splitlines()

    assert len(output_lines) == 4
