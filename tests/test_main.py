import main


def sample_transactions() -> list[dict]:
    """Возвращает тестовые банковские операции."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-15T10:30:00",
            "description": "Перевод организации",
            "from": "Счёт 1",
            "to": "Счёт 2",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2024-01-10T12:00:00",
            "description": "Покупка в магазине",
            "from": "Счёт 3",
            "to": "Магазин",
            "operationAmount": {
                "amount": "500.00",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
        },
    ]


def test_load_transactions_json(monkeypatch) -> None:
    """Проверяет загрузку JSON."""
    expected = sample_transactions()

    monkeypatch.setattr(
        main,
        "get_financial_data",
        lambda _path: expected,
    )

    assert main.load_transactions("1") == expected


def test_load_transactions_csv(monkeypatch) -> None:
    """Проверяет загрузку CSV."""
    expected = sample_transactions()

    monkeypatch.setattr(
        main,
        "read_transactions_from_csv",
        lambda _path: expected,
    )

    assert main.load_transactions("2") == expected


def test_load_transactions_excel(monkeypatch) -> None:
    """Проверяет загрузку XLSX."""
    expected = sample_transactions()

    monkeypatch.setattr(
        main,
        "read_transactions_from_excel",
        lambda _path: expected,
    )

    assert main.load_transactions("3") == expected


def test_load_transactions_invalid_type() -> None:
    """Проверяет неизвестный тип файла."""
    assert main.load_transactions("9") == []


def test_load_transactions_empty_result(monkeypatch) -> None:
    """Проверяет обработку пустого результата загрузки."""
    monkeypatch.setattr(
        main,
        "get_financial_data",
        lambda _path: [],
    )

    assert main.load_transactions("1") == []


def test_load_transactions_non_list(monkeypatch) -> None:
    """Проверяет обработку результата не в виде списка."""
    monkeypatch.setattr(
        main,
        "get_financial_data",
        lambda _path: {"operation": "test"},
    )

    assert main.load_transactions("1") == []


def test_load_transactions_error(monkeypatch, capsys) -> None:
    """Проверяет обработку ошибки чтения файла."""

    def raise_error(_path: str) -> None:
        raise OSError("Файл не найден")

    monkeypatch.setattr(
        main,
        "get_financial_data",
        raise_error,
    )

    assert main.load_transactions("1") == []
    assert "Не удалось прочитать файл" in capsys.readouterr().out


def test_is_ruble_transaction_true() -> None:
    """Проверяет определение операции в рублях."""
    transaction = sample_transactions()[0]

    assert main.is_ruble_transaction(transaction) is True


def test_is_ruble_transaction_false() -> None:
    """Проверяет операцию в иностранной валюте."""
    transaction = sample_transactions()[1]

    assert main.is_ruble_transaction(transaction) is False


def test_is_ruble_transaction_invalid_currency() -> None:
    """Проверяет операцию с некорректной валютой."""
    transaction = {"operationAmount": {"currency": "RUB"}}

    assert main.is_ruble_transaction(transaction) is False


def test_is_ruble_transaction_missing_amount() -> None:
    """Проверяет операцию без информации о валюте."""
    assert main.is_ruble_transaction({}) is False


def test_format_transaction() -> None:
    """Проверяет форматирование операции."""
    result = main.format_transaction(sample_transactions()[0])

    assert "15.01.2024" in result
    assert "Перевод организации" in result
    assert "Счёт 1 -> Счёт 2" in result
    assert "1000.00" in result
    assert "руб." in result


def test_format_transaction_missing_fields() -> None:
    """Проверяет форматирование операции без данных."""
    result = main.format_transaction({})

    assert "Дата неизвестна" in result
    assert "Без описания" in result


def test_format_transaction_invalid_date() -> None:
    """Проверяет форматирование с некорректной датой."""
    result = main.format_transaction(
        {"date": "неверная дата", "description": "Проверка"}
    )

    assert "неверная дата" in result


def test_ask_yes_no_yes(monkeypatch) -> None:
    """Проверяет положительный ответ пользователя."""
    monkeypatch.setattr("builtins.input", lambda _prompt: "да")

    assert main.ask_yes_no("Продолжить?") is True


def test_ask_yes_no_no(monkeypatch) -> None:
    """Проверяет отрицательный ответ пользователя."""
    monkeypatch.setattr("builtins.input", lambda _prompt: "нет")

    assert main.ask_yes_no("Продолжить?") is False


def test_ask_yes_no_invalid_then_valid(monkeypatch, capsys) -> None:
    """Проверяет повторный ввод после неправильного ответа."""
    answers = iter(["может быть", "да"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(answers),
    )

    assert main.ask_yes_no("Продолжить?") is True
    assert "Введите Да или Нет." in capsys.readouterr().out


def test_main_success(monkeypatch, capsys) -> None:
    """Проверяет основной сценарий работы программы."""
    monkeypatch.setattr(
        main,
        "load_transactions",
        lambda _file_type: sample_transactions(),
    )

    answers = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(answers),
    )

    main.main()

    output = capsys.readouterr().out

    assert "Для обработки выбран JSON-файл." in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "Перевод организации" in output


def test_main_invalid_file_choice(monkeypatch, capsys) -> None:
    """Проверяет повторный запрос при неправильном выборе файла."""
    monkeypatch.setattr(
        main,
        "load_transactions",
        lambda _file_type: [],
    )

    answers = iter(["9", "1"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(answers),
    )

    main.main()

    output = capsys.readouterr().out

    assert "Неверный пункт меню" in output
    assert "Не найдено ни одной транзакции" in output


def test_main_empty_file(monkeypatch, capsys) -> None:
    """Проверяет завершение при пустом файле."""
    monkeypatch.setattr(main, "load_transactions", lambda _file_type: [])

    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: "1",
    )

    main.main()

    assert (
        "Не найдено ни одной транзакции в выбранном файле."
        in capsys.readouterr().out
    )


def test_main_invalid_status_then_valid(monkeypatch, capsys) -> None:
    """Проверяет повторный ввод неизвестного статуса."""
    monkeypatch.setattr(
        main,
        "load_transactions",
        lambda _file_type: sample_transactions(),
    )

    answers = iter(
        ["1", "UNKNOWN", "EXECUTED", "нет", "нет", "нет"]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(answers),
    )

    main.main()

    output = capsys.readouterr().out

    assert 'Статус операции "UNKNOWN" недоступен.' in output
    assert "Перевод организации" in output


def test_main_no_matching_transactions(monkeypatch, capsys) -> None:
    """Проверяет сообщение при отсутствии операций нужного статуса."""
    monkeypatch.setattr(
        main,
        "load_transactions",
        lambda _file_type: sample_transactions(),
    )

    answers = iter(["1", "PENDING", "нет", "нет", "нет"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(answers),
    )

    main.main()

    assert (
        "Не найдено ни одной транзакции, подходящей"
        in capsys.readouterr().out
    )


def test_main_search_no_matches(monkeypatch, capsys) -> None:
    """Проверяет поиск, который не находит операции."""
    monkeypatch.setattr(
        main,
        "load_transactions",
        lambda _file_type: sample_transactions(),
    )

    answers = iter(
        ["1", "EXECUTED", "нет", "нет", "да", "несуществующее"]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(answers),
    )

    main.main()

    assert (
        "Не найдено ни одной транзакции, подходящей"
        in capsys.readouterr().out
    )
