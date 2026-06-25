import csv
from pathlib import Path


def build_daily_fraud_summary(input_file: Path, output_file: Path) -> dict:
    """
    Build a small fraud monitoring summary from flagged transaction data.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    total_transactions = 0
    fraud_transactions = 0
    high_amount_transactions = 0
    credit_card_transactions = 0
    total_transaction_amount = 0.0

    with input_file.open("r", encoding="utf-8", newline="") as input_csv:
        reader = csv.DictReader(input_csv)

        for row in reader:
            total_transactions += 1
            total_transaction_amount += float(row["TransactionAmt"])

            if row.get("labeled_fraud") == "True":
                fraud_transactions += 1

            if row.get("high_transaction_amount") == "True":
                high_amount_transactions += 1

            if row.get("credit_card_transaction") == "True":
                credit_card_transactions += 1

    fraud_rate = fraud_transactions / total_transactions if total_transactions else 0

    summary_row = {
        "total_transactions": total_transactions,
        "fraud_transactions": fraud_transactions,
        "fraud_rate": round(fraud_rate, 4),
        "high_amount_transactions": high_amount_transactions,
        "credit_card_transactions": credit_card_transactions,
        "total_transaction_amount": round(total_transaction_amount, 2),
    }

    with output_file.open("w", encoding="utf-8", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=list(summary_row.keys()))
        writer.writeheader()
        writer.writerow(summary_row)

    return {
        "input_file": str(input_file),
        "output_file": str(output_file),
        **summary_row,
    }
