# Виджет банковских операций

Проект представляет собой набор утилит для фильтрации и сортировки финансовых транзакций клиента.

## Инструкция по установке и использованию

1. Клонируйте репозиторий на свой компьютер.
2. Установите зависимости проекта:

   ```bash
   poetry install
   ```

3. Импортируйте необходимые функции:

   ```python
   from src.processing import filter_by_state, sort_by_date

   # Фильтрация
   executed_ops = filter_by_state(data, "EXECUTED")

   # Сортировка
   sorted_ops = sort_by_date(data)
   ```

## Работа с финансовыми транзакциями

Добавлена поддержка чтения финансовых операций из CSV- и Excel-файлов.

- `read_transactions_from_csv(file_path)` — чтение CSV.
- `read_transactions_from_excel(file_path)` — чтение Excel.

Функции возвращают список словарей с транзакциями.

## Тестирование

Запуск тестов:

```bash
poetry run pytest
```

Проверка покрытия:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```





