from unittest.mock import Mock, patch

import requests

from src.external_api import convert_to_rub


def test_convert_to_rub_currency_rub() -> None:
    """Проверка конвертации, если транзакция уже в рублях (запрос к API не отправляется)."""
    transaction = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {"code": "RUB"}
        }
    }
    assert convert_to_rub(transaction) == 1000.50


@patch("src.external_api.requests.get")
def test_convert_to_rub_usd_success(mock_get: Mock) -> None:
    """Проверка успешной конвертации USD в RUB с подменой ответа API."""
    # Настраиваем фейковый ответ от сервера
    mock_response = Mock()
    mock_response.json.return_value = {"result": 8500.0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 8500.0
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_convert_to_rub_api_error(mock_get: Mock) -> None:
    """Проверка возврата 0.0 при возникновении сетевой ошибки API."""
    mock_get.side_effect = requests.RequestException

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "EUR"}
        }
    }

    assert convert_to_rub(transaction) == 0.0


def test_convert_to_rub_empty_transaction() -> None:
    """Проверка обработки пустой транзакции."""
    assert convert_to_rub({}) == 0.0
