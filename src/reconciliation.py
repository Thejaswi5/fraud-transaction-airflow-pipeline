import csv
from pathlib import Path


def count_csv_rows(file_path: Path) -> int:
    """
    Count data rows in a CSV file, excluding the header row.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)

        try:
            next(reader)
        except StopIteration:
            return 0

        return sum(1 for _ in reader)


def reconcile_row_counts(source_file: Path, target_file: Path) -> dict:
    """
    Compare source and target CSV row counts.

    Raises an error if the counts do not match.
    """
    source_count = count_csv_rows(source_file)
    target_count = count_csv_rows(target_file)

    if source_count != target_count:
        raise ValueError(
            f"Row count mismatch: source={source_count}, target={target_count}"
        )

    return {
        "source_file": str(source_file),
        "target_file": str(target_file),
        "source_count": source_count,
        "target_count": target_count,
        "status": "matched",
    }
