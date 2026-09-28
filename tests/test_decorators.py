import pytest

from src.decorators import log


def test_log_console_success(capsys):
    """Проверка успешного выполнения функции с выводом в консоль."""
    @log()
    def add(x, y):
        return x + y

    add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_console_error(capsys):
    """Проверка логирования ошибки в консоль."""
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out


def test_log_file_success(tmp_path):
    """Проверка успешного выполнения функции с записью в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(x, y):
        return x * y

    multiply(3, 4)
    content = log_file.read_text(encoding="utf-8")
    assert "multiply ok" in content


def test_log_file_error(tmp_path):
    """Проверка логирования ошибки с записью в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def error_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        error_func()

    content = log_file.read_text(encoding="utf-8")
    assert "error_func error: ValueError. Inputs: (), {}" in content
