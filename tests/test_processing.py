from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state() -> None:
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"}
    ]
    assert filter_by_state(data, "EXECUTED") == [{"id": 1, "state": "EXECUTED"}]
@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 0),
    ],
)
def test_filter_by_state(
    sample_transactions: List[Dict[str, Any]], state: str, expected_count: int
) -> None:
    """Проверка фильтрации операций по различным статусам."""
    result = filter_by_state(sample_transactions, state)
    assert len(result) == expected_count


def test_sort_by_date_descending(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка сортировки операций по дате по убыванию."""
    sorted_data = sort_by_date(sample_transactions, reverse=True)
    assert sorted_data[0]["id"] == 41428829
    assert sorted_data[-1]["id"] == 594226727

def test_sort_by_date() -> None:
    data = [
        {"id": 1, "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "date": "2021-07-03T18:35:29.512364"}
    ]
    result = sort_by_date(data)
    assert result[0]["id"] == 2

def test_sort_by_date_ascending(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка сортировки операций по дате по возрастанию."""
    sorted_data = sort_by_date(sample_transactions, reverse=False)
    assert sorted_data[0]["id"] == 594226727
    assert sorted_data[-1]["id"] == 41428829
