from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования выполнения функции.

    Записывает имя функции и результат при успешном выполнении,
    либо имя функции, тип ошибки и аргументы при ошибке.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                error_type = e.__class__.__name__
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"
                _write_log(log_message, filename)
                raise e

        return wrapper
    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Вспомогательная функция для записи лога в файл или вывода в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
