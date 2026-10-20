import pandas as pd


def read_transactions_from_csv(file_path: str) -> list[dict]:
    """Считывает транзакции из CSV-файла."""
    transactions = pd.read_csv(file_path)
    return transactions.to_dict(orient="records")


def read_transactions_from_excel(file_path: str) -> list[dict]:
    """Считывает транзакции из Excel-файла."""
    transactions = pd.read_excel(file_path)
    return transactions.to_dict(orient="records")
