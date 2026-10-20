from typing import Any, Dict, List

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура, возвращающая тестовый список транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]


# Тестирование filter_by_currency

@pytest.mark.parametrize("currency, expected_count", [
    ("USD", 2),
    ("RUB", 1),
    ("EUR", 0),  # Случай, когда валюта отсутствует в списке
])
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], currency: str, expected_count: int) -> None:
    """Проверка фильтрации по различным валютам."""
    result = list(filter_by_currency(sample_transactions, currency))
    assert len(result) == expected_count


def test_filter_by_currency_empty_list() -> None:
    """Проверка обработки пустого списка транзакций."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


# Тестирование transaction_descriptions

def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка получения описаний всех транзакций по очереди."""
    gen = transaction_descriptions(sample_transactions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод со счета на счет"


def test_transaction_descriptions_empty() -> None:
    """Проверка генератора описаний на пустом списке."""
    result = list(transaction_descriptions([]))
    assert result == []


# Тестирование card_number_generator

@pytest.mark.parametrize("start, stop, expected", [
    (1, 3, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]),
    (5, 5, ["0000 0000 0000 0005"]),  # Крайний случай: диапазон из 1 элемента
])
def test_card_number_generator(start: int, stop: int, expected: List[str]) -> None:
    """Проверка генерации номеров карт и их форматирования."""
    result = list(card_number_generator(start, stop))
    assert result == expected
