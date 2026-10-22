# Трекер самолётов

Курсовой проект: программа собирает данные о самолётах, находящихся
в воздушном пространстве выбранной страны, с помощью API
**nominatim.openstreetmap.org** (координаты страны) и
**opensky-network.org** (данные о самолётах), сохраняет их в JSON-файл
и выводит отфильтрованные и отсортированные данные в консоль.

## Структура проекта

```
aircraft_tracker/
├── data/                # JSON-хранилище самолётов
├── src/
│   ├── api.py           # абстрактный класс BaseAPI и AeroplanesAPI
│   ├── aeroplane.py     # класс Aeroplane
│   ├── filters.py       # фильтрация, сортировка, топ-N
│   └── storage.py       # BaseSaver и JSONSaver
├── tests/               # тесты pytest
├── main.py              # взаимодействие с пользователем
├── pyproject.toml       # poetry, pytest, coverage, isort
└── requirements.txt
```

## Установка и запуск

```bash
pip install -r requirements.txt
python main.py
```

Программа попросит:
1. название страны (например, `Spain`);
2. количество самолётов для вывода в топ N;
3. страны для фильтрации по регистрации (через запятую);
4. диапазон высот (например, `10000 - 15000`).

Результат выводится в консоль и сохраняется в `data/aeroplanes.json`.

## Реализация (ООП)

- **`src/api.py`** — абстрактный класс `BaseAPI` (`ABC`,
  `@abstractmethod`) и наследник `AeroplanesAPI`, который получает
  координаты страны (`get_country_bounding_box`) и данные о самолётах
  (`get_aeroplanes`) с обработкой исключений;
- **`src/aeroplane.py`** — класс `Aeroplane` (инкапсуляция): атрибуты
  `callsign`, `country`, `velocity`, `altitude` с валидацией; сравнение
  самолётов по скорости и высоте (`is_faster_than`, `is_higher_than`,
  операции сравнения); `cast_to_object_list` преобразует данные API
  в объекты;
- **`src/filters.py`** — фильтрация по стране регистрации и диапазону
  высот, сортировка по высоте по убыванию, выбор топ-N;
- **`src/storage.py`** — абстрактный класс `BaseSaver` (`add_aeroplane`,
  `get_aeroplanes`, `delete_aeroplane`) и `JSONSaver` для работы
  с JSON-файлом.

## Тестирование

```bash
pytest
pytest --cov=src --cov-report=term-missing
```

Покрытие функционального кода — не менее 70 %.

## Проверка стиля

```bash
flake8 src tests main.py
isort --check-only src tests main.py
mypy src
```
