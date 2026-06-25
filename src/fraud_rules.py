import csv
from pathlib import Path


def create_fraud_risk_flags(
    input_file: Path,
    output_file: Path,
    high_amount_threshold: float = 1000.0,
) -> dict:
    """
    Create simple fraud-risk flags from processed transaction data.

    The rules are intentionally simple and auditable:
    - high_transaction_amount: transaction amount is greater than or equal to threshold
    - labeled_fraud: source fraud label is 1
    - missing_payer_email_domain: payer email domain is empty
    - credit_card_transaction: card6 is credit
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    rows_written = 0
    high_amount_count = 0
    labeled_fraud_count = 0
    credit_card_count = 0

    with input_file.open("r", encoding="utf-8", newline="") as input_csv:
        reader = csv.DictReader(input_csv)

        output_columns = list(reader.fieldnames or []) + [
            "high_transaction_amount",
            "labeled_fraud",
            "missing_payer_email_domain",
            "credit_card_transaction",
        ]

        with output_file.open("w", encoding="utf-8", newline="") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=output_columns)
            writer.writeheader()

            for row in reader:
                transaction_amount = float(row["TransactionAmt"])
                payer_email_domain = row.get("P_emaildomain", "")
                card_type = row.get("card6", "")
                fraud_label = row.get("isFraud", "0")

                high_transaction_amount = transaction_amount >= high_amount_threshold
                labeled_fraud = fraud_label == "1"
                missing_payer_email_domain = payer_email_domain == ""
                credit_card_transaction = card_type.lower() == "credit"

                row["high_transaction_amount"] = str(high_transaction_amount)
                row["labeled_fraud"] = str(labeled_fraud)
                row["missing_payer_email_domain"] = str(missing_payer_email_domain)
                row["credit_card_transaction"] = str(credit_card_transaction)

                writer.writerow(row)
                rows_written += 1

                high_amount_count += int(high_transaction_amount)
                labeled_fraud_count += int(labeled_fraud)
                credit_card_count += int(credit_card_transaction)

    return {
        "input_file": str(input_file),
        "output_file": str(output_file),
        "rows_written": rows_written,
        "high_amount_count": high_amount_count,
        "labeled_fraud_count": labeled_fraud_count,
        "credit_card_count": credit_card_count,
    }
