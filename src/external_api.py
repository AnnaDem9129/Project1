import os
from typing import Any

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """Принимает словарь с транзакцией и возвращает сумму операции в рублях.

    Если валюта операции USD или EUR, делает запрос к Exchange Rates Data API.
    """
    operation_amount = transaction.get("operationAmount", {})
    if not operation_amount:
        return 0.0

    amount = float(operation_amount.get("amount", 0.0))
    currency_code = operation_amount.get("currency", {}).get("code")

    # Если сумма уже в рублях, возвращаем ее без обращения к API
    if currency_code == "RUB":
        return amount

    # Если валюта USD или EUR, отправляем запрос к API
    if currency_code in ["USD", "EUR"]:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return float(data.get("result", 0.0))
        except (requests.RequestException, KeyError, ValueError):
            return 0.0

    return amount
