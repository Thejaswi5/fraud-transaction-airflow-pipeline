import csv
from pathlib import Path
from typing import Iterable


def validate_source_file(file_path: Path, required_columns: Iterable[str], min_rows: int = 1) -> dict:
    """
    Validate that a source CSV file exists, is readable, contains required columns,
    and has at least the expected minimum number of data rows.

    This function is designed to run as the first validation gate in an Airflow DAG.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")

    if file_path.stat().st_size == 0:
        raise ValueError(f"Source file is empty: {file_path}")

    required_columns = list(required_columns)

    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)

        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"Source file has no header row: {file_path}")

        missing_columns = sorted(set(required_columns) - set(header))
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        row_count = sum(1 for _ in reader)

    if row_count < min_rows:
        raise ValueError(
            f"Source file has {row_count} data rows, expected at least {min_rows}"
        )

    return {
        "file_path": str(file_path),
        "file_size_bytes": file_path.stat().st_size,
        "row_count": row_count,
        "required_columns_found": len(required_columns),
    }
