import pytest

from src.processing import (
    filter_by_state,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)


@pytest.fixture
def transactions() -> list[dict]:
    """Создаёт тестовый список транзакций."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-03T10:00:00",
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2024-01-01T10:00:00",
            "description": "Открытие вклада",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-02T10:00:00",
            "description": "Перевод организации",
        },
    ]


def test_filter_by_state_default(
    transactions: list[dict],
) -> None:
    """Проверяет фильтрацию по статусу по умолчанию."""
    result = filter_by_state(transactions)

    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_custom(
    transactions: list[dict],
) -> None:
    """Проверяет фильтрацию по заданному статусу."""
    result = filter_by_state(transactions, "CANCELED")

    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_state_case_insensitive(
    transactions: list[dict],
) -> None:
    """Проверяет, что регистр статуса не имеет значения."""
    result = filter_by_state(transactions, "executed")

    assert len(result) == 2


def test_filter_by_state_empty() -> None:
    """Проверяет фильтрацию пустого списка."""
    assert filter_by_state([]) == []


def test_sort_by_date_descending(
    transactions: list[dict],
) -> None:
    """Проверяет сортировку по убыванию даты."""
    result = sort_by_date(transactions)

    assert [item["id"] for item in result] == [1, 3, 2]


def test_sort_by_date_ascending(
    transactions: list[dict],
) -> None:
    """Проверяет сортировку по возрастанию даты."""
    result = sort_by_date(transactions, reverse=False)

    assert [item["id"] for item in result] == [2, 3, 1]


def test_sort_by_date_empty() -> None:
    """Проверяет сортировку пустого списка."""
    assert sort_by_date([]) == []


def test_process_bank_search(
    transactions: list[dict],
) -> None:
    """Проверяет поиск по описанию."""
    result = process_bank_search(
        transactions,
        "Перевод",
    )

    assert len(result) == 2
    assert all(
        "Перевод" in item["description"]
        for item in result
    )


def test_process_bank_search_case_insensitive(
    transactions: list[dict],
) -> None:
    """Проверяет поиск без учёта регистра."""
    result = process_bank_search(
        transactions,
        "перЕвод",
    )

    assert len(result) == 2


def test_process_bank_search_no_matches(
    transactions: list[dict],
) -> None:
    """Проверяет поиск без совпадений."""
    assert process_bank_search(
        transactions,
        "несуществующее слово",
    ) == []


def test_process_bank_search_special_characters() -> None:
    """Проверяет поиск текста со специальными символами."""
    data = [
        {"description": "Платёж (магазин)"},
        {"description": "Платёж магазин"},
    ]

    result = process_bank_search(data, "(магазин)")

    assert len(result) == 1
    assert result[0]["description"] == "Платёж (магазин)"


def test_process_bank_search_empty_query(
    transactions: list[dict],
) -> None:
    """Проверяет поиск с пустой строкой."""
    result = process_bank_search(transactions, "")

    assert result == transactions
    assert result is not transactions


def test_process_bank_search_missing_description() -> None:
    """Проверяет поиск в операциях без описания."""
    data = [{"id": 1}, {"id": 2, "description": "Перевод"}]

    result = process_bank_search(data, "перевод")

    assert result == [{"id": 2, "description": "Перевод"}]


def test_process_bank_operations(
    transactions: list[dict],
) -> None:
    """Проверяет подсчёт операций по описаниям."""
    result = process_bank_operations(
        transactions,
        ["Перевод организации", "Открытие вклада"],
    )

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
    }


def test_process_bank_operations_missing_description() -> None:
    """Пропускает операции без текстового описания."""
    data = [
        {"id": 1, "description": "Перевод"},
        {"id": 2},
        {"id": 3, "description": None},
    ]

    result = process_bank_operations(
        data,
        ["Перевод", "Покупка"],
    )

    assert result == {"Перевод": 1, "Покупка": 0}


def test_process_bank_operations_empty_data() -> None:
    """Проверяет подсчёт для пустого списка операций."""
    result = process_bank_operations(
        [],
        ["Перевод", "Покупка"],
    )

    assert result == {"Перевод": 0, "Покупка": 0}


def test_process_bank_operations_empty_categories(
    transactions: list[dict],
) -> None:
    """Проверяет вызов без списка категорий."""
    assert process_bank_operations(transactions, []) == {}
