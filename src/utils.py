import json
from typing import Any


def get_financial_data(path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл с финансовыми транзакциями и возвращает список словарей.

    Если файл не найден, пустой или содержит данные не в формате списка,
    возвращает пустой список.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
