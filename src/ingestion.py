import csv
from pathlib import Path
from typing import Iterable


def ingest_transactions(
    source_file: Path,
    output_file: Path,
    selected_columns: Iterable[str],
) -> dict:
    """
    Ingest selected transaction columns from a source CSV into a processed CSV.

    This implementation is idempotent for local batch processing because it rewrites
    the output file on every run instead of appending to it.
    """
    source_file = Path(source_file)
    output_file = Path(output_file)
    selected_columns = list(selected_columns)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with source_file.open("r", encoding="utf-8", newline="") as input_csv:
        reader = csv.DictReader(input_csv)

        missing_columns = sorted(set(selected_columns) - set(reader.fieldnames or []))
        if missing_columns:
            raise ValueError(f"Cannot ingest. Missing columns: {missing_columns}")

        rows_written = 0

        with output_file.open("w", encoding="utf-8", newline="") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=selected_columns)
            writer.writeheader()

            for row in reader:
                writer.writerow({column: row[column] for column in selected_columns})
                rows_written += 1

    return {
        "source_file": str(source_file),
        "output_file": str(output_file),
        "rows_written": rows_written,
        "columns_written": len(selected_columns),
    }
