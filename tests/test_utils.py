from unittest.mock import mock_open, patch

from src.utils import get_financial_data


def test_get_financial_data_valid() -> None:
    """Проверка успешного чтения валидного JSON-файла."""
    mock_data = '[{"id": 1, "state": "EXECUTED"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_financial_data("data/operations.json")
        assert result == [{"id": 1, "state": "EXECUTED"}]


def test_get_financial_data_file_not_found() -> None:
    """Проверка обработки ситуации, когда файл не найден."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = get_financial_data("non_existent_file.json")
        assert result == []


def test_get_financial_data_invalid_json() -> None:
    """Проверка обработки некорректного или пустого JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = get_financial_data("corrupted.json")
        assert result == []


def test_get_financial_data_not_a_list() -> None:
    """Проверка возврата пустого списка, если в JSON лежит словарь вместо списка."""
    mock_data = '{"id": 1, "state": "EXECUTED"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_financial_data("dict.json")
        assert result == []
