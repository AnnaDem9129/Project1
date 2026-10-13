import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты."""
    logger.info("Запуск маскирования номера карты")
    try:
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info("Номер карты успешно замаскирован")
        return masked
    except Exception as e:
        logger.error(f"Ошибка при маскировании номера карты: {e}")
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета."""
    logger.info("Запуск маскирования номера счета")
    try:
        masked = f"**{account_number[-4:]}"
        logger.info("Номер счета успешно замаскирован")
        return masked
    except Exception as e:
        logger.error(f"Ошибка при маскировании номера счета: {e}")
        raise
