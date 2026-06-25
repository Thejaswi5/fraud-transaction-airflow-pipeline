from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
LOG_DIR = PROJECT_ROOT / "logs"

RAW_TRANSACTION_FILE = RAW_DATA_DIR / "train_transaction.csv"
PROCESSED_TRANSACTION_FILE = PROCESSED_DATA_DIR / "daily_transactions.csv"
FRAUD_SUMMARY_FILE = PROCESSED_DATA_DIR / "daily_fraud_summary.csv"

REQUIRED_COLUMNS = [
    "TransactionID",
    "isFraud",
    "TransactionDT",
    "TransactionAmt",
    "ProductCD",
    "card1",
    "card2",
    "card3",
    "card4",
    "card5",
    "card6",
    "P_emaildomain",
    "R_emaildomain",
]

FRAUD_LABEL_COLUMN = "isFraud"
TRANSACTION_ID_COLUMN = "TransactionID"
TRANSACTION_AMOUNT_COLUMN = "TransactionAmt"

MAX_TRANSACTION_AMOUNT = 50000
MIN_EXPECTED_ROWS = 1
