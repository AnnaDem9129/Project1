# Виджет банковских операций

Проект представляет собой набор утилит для обработки, фильтрации, сортировки, маскирования персональных данных и логирования банковских транзакций.

## Описание модулей

- `src/masks.py` — маскирование номеров банковских карт и счетов.
- `src/widget.py` — маскирование входных данных и форматирование дат.
- `src/processing.py` — фильтрация транзакций по статусу (`EXECUTED`, `CANCELED`) и сортировка по дате.
- `src/generators.py` — генераторы для фильтрации по валюте, получения описаний транзакций и создания номеров карт.
- `src/decorators.py` — декоратор `@log` для автоматического логирования вызовов функций, результатов и ошибок в файл или консоль.

## Установка и использование

1. Клонируйте репозиторий на свой ПК:
```bash
git clone <URL_вашего_репозитория>
```

2. Установите зависимости проекта с помощью Poetry:
```bash
poetry install
```

3. Пример использования функций:

```python
from src.processing import filter_by_state, sort_by_date
from src.generators import card_number_generator
from src.decorators import log

# Логирование работы функции в файл
@log(filename="mylog.txt")
def add_numbers(a, b):
    return a + b

# Пример работы с транзакциями
executed_ops = filter_by_state(data, 'EXECUTED')
sorted_ops = sort_by_date(data)

# Генерация номеров карт
for card in card_number_generator(1, 3):
    print(card)
```

## Тестирование и качество кода

Для запуска модульных тестов и проверки покрытия:

```bash
# Запуск тестов
pytest

# Запуск тестов с проверкой покрытия
pytest --cov=src --cov-report=html
```

Для проверки соблюдения стандартов PEP 8 и сортировки импортов:

```bash
# Проверка стиля
flake8 src/ tests/

# Сортировка импортов
isort src/ tests/
```