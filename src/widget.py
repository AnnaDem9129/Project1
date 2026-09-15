"""Модуль для работы с виджетами банковских операций."""
import datetime
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    if not info or len(info.split()) < 2:
        return "Некорректный ввод"

    parts = info.split()
    number = parts[-1]
    name_parts = parts[:-1]
    name = " ".join(name_parts)

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    date_obj = datetime.datetime.fromisoformat(date_string)
    return date_obj.strftime("%d.%m.%Y")
