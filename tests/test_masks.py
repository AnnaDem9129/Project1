import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тест маскирования номера карты."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("", ""),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Проверка правильности маскирования номера карты с параметризацией."""
    assert get_mask_card_number(card_number) == expected


def test_get_mask_account() -> None:
    """Тест маскирования номера счета."""
    assert get_mask_account("73654108430135874305") == "**4305"
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("12345", "**2345"),
        ("", ""),
    ],
)
def test_get_mask_account(account_number: str, expected: str) -> None:
    """Проверка маскирования номера счета и граничных случаев."""
    assert get_mask_account(account_number) == expected
