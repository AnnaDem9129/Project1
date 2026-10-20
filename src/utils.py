import json
import logging
import os
from typing import Any

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_financial_data(path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл с финансовыми транзакциями и возвращает список словарей.

    Если файл не найден, пустой или содержит данные не в формате списка,
    возвращает пустой список.
    """
    """Читает JSON-файл с финансовыми транзакциями и возвращает список словарей."""
    logger.info(f"Попытка чтения файла по пути: {path}")
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Файл успешно прочитан, загружено элементов: {len(data)}")
                return data
            logger.warning("Содержимое файла не является списком")
            return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка при чтении файла {path}: {e}")
        return []
