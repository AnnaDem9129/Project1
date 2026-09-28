from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """Принимает список транзакций и код валюты, возвращает итератор по транзакциям с указанной валютой."""
    for transaction in transactions:
        if (
            transaction.get("operationAmount", {})
            .get("currency", {})
            .get("code") == currency_code
        ):
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Возвращает описание каждой транзакции по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера карт формата XXXX XXXX XXXX XXXX в заданном диапазоне."""
    for number in range(start, stop + 1):
        card_str = f"{number:016d}"
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted_card
