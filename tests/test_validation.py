from pathlib import Path

import pytest

from config.settings import REQUIRED_COLUMNS, MIN_EXPECTED_ROWS
from src.validation import validate_source_file


def test_validate_source_file_accepts_valid_fixture():
    sample_file = Path("tests/fixtures/valid_transactions_sample.csv")

    result = validate_source_file(
        sample_file,
        REQUIRED_COLUMNS,
        MIN_EXPECTED_ROWS,
    )

    assert result["row_count"] == 3
    assert result["required_columns_found"] == len(REQUIRED_COLUMNS)
    assert result["file_size_bytes"] > 0


def test_validate_source_file_rejects_missing_columns_fixture():
    sample_file = Path("tests/fixtures/missing_columns_transactions_sample.csv")

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_source_file(
            sample_file,
            REQUIRED_COLUMNS,
            MIN_EXPECTED_ROWS,
        )
