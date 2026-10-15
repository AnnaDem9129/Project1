from unittest.mock import Mock, patch

import pandas as pd

from src.file_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


@patch("src.file_readers.pd.read_csv")
def test_read_transactions_from_csv(mock_read_csv: Mock) -> None:
    """Проверяет чтение транзакций из CSV с помощью Mock."""
    expected = [{"id": 1, "amount": 1000}]

    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = expected
    mock_read_csv.return_value = mock_dataframe

    result = read_transactions_from_csv("transactions.csv")

    mock_read_csv.assert_called_once_with("transactions.csv")
    mock_dataframe.to_dict.assert_called_once_with(orient="records")
    assert result == expected


@patch("src.file_readers.pd.read_excel")
def test_read_transactions_from_excel(mock_read_excel: Mock) -> None:
    """Проверяет чтение транзакций из Excel с помощью Mock."""
    expected = [{"id": 1, "amount": 1000}]

    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = expected
    mock_read_excel.return_value = mock_dataframe

    result = read_transactions_from_excel("transactions.xlsx")

    mock_read_excel.assert_called_once_with("transactions.xlsx")
    mock_dataframe.to_dict.assert_called_once_with(orient="records")
    assert result == expected


def test_read_transactions_from_csv_real_file(tmp_path) -> None:
    """Проверяет чтение настоящего CSV-файла."""
    file_path = tmp_path / "transactions.csv"
    pd.DataFrame([{"id": 1, "amount": 1000}]).to_csv(
        file_path, index=False
    )

    result = read_transactions_from_csv(str(file_path))

    assert result == [{"id": 1, "amount": 1000}]


def test_read_transactions_from_excel_real_file(tmp_path) -> None:
    """Проверяет чтение настоящего Excel-файла."""
    file_path = tmp_path / "transactions.xlsx"
    pd.DataFrame([{"id": 1, "amount": 1000}]).to_excel(
        file_path, index=False
    )

    result = read_transactions_from_excel(str(file_path))

    assert result == [{"id": 1, "amount": 1000}]
