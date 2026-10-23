from datetime import datetime
from pathlib import Path
from typing import Any

from src.file_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)
from src.processing import (
    filter_by_state,
    process_bank_search,
    sort_by_date,
)
from src.utils import get_financial_data

BASE_DIR = Path(__file__).resolve().parent

FILE_OPTIONS = {
    "1": ("JSON", BASE_DIR / "data" / "operations.json"),
    "2": ("CSV", BASE_DIR / "data" / "transactions.csv"),
    "3": ("XLSX", BASE_DIR / "data" / "transactions_excel.xlsx"),
}

AVAILABLE_STATUSES = ("EXECUTED", "CANCELED", "PENDING")


def load_transactions(file_type: str) -> list[dict[str, Any]]:
    """Загружает транзакции из выбранного файла."""
    if file_type not in FILE_OPTIONS:
        return []

    _, file_path = FILE_OPTIONS[file_type]

    try:
        if file_type == "1":
            data = get_financial_data(str(file_path))
        elif file_type == "2":
            data = read_transactions_from_csv(str(file_path))
        else:
            data = read_transactions_from_excel(str(file_path))

        if isinstance(data, list):
            return [
                item for item in data
                if isinstance(item, dict)
            ]

        return []

    except (OSError, ValueError, TypeError) as error:
        print(f"Не удалось прочитать файл: {error}")
        return []


def is_ruble_transaction(transaction: dict[str, Any]) -> bool:
    """Проверяет, указаны ли рубли в валюте операции."""
    operation_amount = transaction.get("operationAmount", {})
    if not isinstance(operation_amount, dict):
        return False

    currency = operation_amount.get("currency", {})
    if not isinstance(currency, dict):
        return False

    code = str(currency.get("code", "")).upper()
    name = str(currency.get("name", "")).lower()

    is_ruble_code = code == "RUB"
    is_ruble_name = name in (
        "руб.",
        "рубль",
        "рубли",
        "рублей",
        "российский рубль",
        "российские рубли",
    )

    return is_ruble_code or is_ruble_name


def format_transaction(transaction: dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода."""
    raw_date = str(transaction.get("date", ""))
    description = str(
        transaction.get("description", "Без описания")
    )

    if raw_date:
        try:
            parsed_date = datetime.fromisoformat(
                raw_date.replace("Z", "+00:00")
            )
            formatted_date = parsed_date.strftime("%d.%m.%Y")
        except ValueError:
            formatted_date = raw_date
    else:
        formatted_date = "Дата неизвестна"

    operation_amount = transaction.get("operationAmount", {})

    if not isinstance(operation_amount, dict):
        operation_amount = {}

    currency = operation_amount.get("currency", {})

    if not isinstance(currency, dict):
        currency = {}

    amount = operation_amount.get(
        "amount",
        transaction.get("amount", ""),
    )
    currency_name = currency.get(
        "name",
        currency.get("code", ""),
    )

    sender = transaction.get("from", "")
    recipient = transaction.get("to", "")

    return (
        f"{formatted_date} {description}\n"
        f"{sender} -> {recipient}\n"
        f"Сумма: {amount} {currency_name}"
    )


def ask_yes_no(question: str) -> bool:
    """Запрашивает у пользователя ответ да или нет."""
    while True:
        answer = input(f"{question} Да/Нет: ").strip().lower()

        if answer in ("да", "д", "yes", "y"):
            return True

        if answer in ("нет", "н", "no", "n"):
            return False

        print("Введите Да или Нет.")


def choose_file_type() -> str:
    """Запрашивает тип файла у пользователя."""
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию из JSON-файла")
    print("2. Получить информацию из CSV-файла")
    print("3. Получить информацию из XLSX-файла")

    while True:
        file_type = input("Ваш выбор: ").strip()
        if file_type in FILE_OPTIONS:
            return file_type
        print("Неверный пункт меню. Выберите 1, 2 или 3.")


def choose_status() -> str:
    """Запрашивает статус транзакций."""
    while True:
        print("Доступные статусы: " + ", ".join(AVAILABLE_STATUSES))
        status = input("Введите статус: ").strip().upper()
        if status in AVAILABLE_STATUSES:
            return status
        print(f'Статус операции "{status}" недоступен.')


def filter_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Применяет фильтры к транзакциям."""
    status = choose_status()
    result = filter_by_state(transactions, status)

    if ask_yes_no("Отсортировать операции по дате?"):
        order = input(
            "Введите «по возрастанию» или «по убыванию»: "
        ).strip().lower()
        result = sort_by_date(
            result,
            reverse=order not in (
                "по возрастанию",
                "возрастание",
                "возрастанию",
            ),
        )

    if ask_yes_no("Выводить только рублёвые транзакции?"):
        result = [
            item for item in result if is_ruble_transaction(item)
        ]

    if ask_yes_no("Искать транзакции по слову в описании?"):
        search = input("Введите слово для поиска: ").strip()
        result = process_bank_search(result, search)

    return result


def print_transactions(
    transactions: list[dict[str, Any]],
) -> None:
    """Выводит список найденных транзакций."""
    print("Распечатываю итоговый список транзакций...")

    if not transactions:
        print(
            "Не найдено ни одной транзакции, подходящей "
            "под ваши условия фильтрации."
        )
        return

    print(
        "Всего банковских операций в выборке: "
        f"{len(transactions)}"
    )

    for transaction in transactions:
        print()
        print(format_transaction(transaction))


def main() -> None:
    """Запускает программу обработки банковских транзакций."""
    print(
        "Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями."
    )

    file_type = choose_file_type()
    print(f"Для обработки выбран {FILE_OPTIONS[file_type][0]}-файл.")

    transactions = load_transactions(file_type)
    if not transactions:
        print("Не найдено ни одной транзакции в выбранном файле.")
        return

    result = filter_transactions(transactions)
    print_transactions(result)


if __name__ == "__main__":
    main()
