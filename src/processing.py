import re
from collections import Counter
from typing import Any


def filter_by_state(
    data: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Фильтрует операции по статусу."""
    normalized_state = state.upper()

    return [
        item
        for item in data
        if str(item.get("state", "")).upper() == normalized_state
    ]


def sort_by_date(
    data: list[dict[str, Any]],
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Сортирует операции по дате."""
    return sorted(
        data,
        key=lambda item: item.get("date", ""),
        reverse=reverse,
    )


def process_bank_search(
    data: list[dict[str, Any]],
    search: str,
) -> list[dict[str, Any]]:
    """Ищет операции по тексту в описании."""
    if not search.strip():
        return data.copy()

    pattern = re.escape(search.strip())

    return [
        item
        for item in data
        if re.search(
            pattern,
            str(item.get("description", "")),
            re.IGNORECASE,
        )
    ]


def process_bank_operations(
    data: list[dict[str, Any]],
    categories: list[str],
) -> dict[str, int]:
    """Подсчитывает количество операций по указанным описаниям."""
    descriptions = Counter(
        item["description"]
        for item in data
        if isinstance(item.get("description"), str)
    )

    return {
        category: descriptions[category]
        for category in categories
    }
