from unittest.mock import mock_open, patch
from src.utils import get_financial_data


def test_get_financial_data_valid() -> None:
    """Тест успешного чтения JSON-файла."""
    mock_data = '[{"id": 1}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_financial_data("dummy_path.json")
        assert result == [{"id": 1}]
