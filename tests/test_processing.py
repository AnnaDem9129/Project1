from src.processing import filter_by_state, sort_by_date


def test_filter_by_state() -> None:
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"}
    ]
    assert filter_by_state(data, "EXECUTED") == [{"id": 1, "state": "EXECUTED"}]


def test_sort_by_date() -> None:
    data = [
        {"id": 1, "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "date": "2021-07-03T18:35:29.512364"}
    ]
    result = sort_by_date(data)
    assert result[0]["id"] == 2