import pytest


@pytest.fixture
def sample_card_number():
    return "7000792289606361"


@pytest.fixture
def sample_account_number():
    return "73654108430135874305"


@pytest.fixture
def sample_transactions():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719410, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "EXECUTED", "date": "2018-03-23T10:45:06.972075"}
    ]
