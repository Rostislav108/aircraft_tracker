"""Тесты функций фильтрации и сортировки."""

from src.aeroplane import Aeroplane
from src.filters import filter_by_altitude, filter_by_country, get_top, sort_by_altitude_desc


def make_aeroplanes() -> list[Aeroplane]:
    """Создаёт набор самолётов для тестов."""
    return [
        Aeroplane("A", "Spain", 250.0, 10000.0),
        Aeroplane("B", "United States", 260.0, 12000.0),
        Aeroplane("C", "Spain", 240.0, 8000.0),
    ]


def test_filter_by_country() -> None:
    """Фильтрует самолёты по стране регистрации."""
    result = filter_by_country(make_aeroplanes(), "Spain")

    assert [aeroplane.callsign for aeroplane in result] == ["A", "C"]


def test_filter_by_country_multiple() -> None:
    """Поддерживает несколько стран через запятую."""
    result = filter_by_country(make_aeroplanes(), "Spain, United States")

    assert len(result) == 3


def test_filter_by_country_empty() -> None:
    """Пустой фильтр возвращает все самолёты."""
    result = filter_by_country(make_aeroplanes(), "")

    assert len(result) == 3


def test_filter_by_altitude() -> None:
    """Фильтрует самолёты по диапазону высот."""
    result = filter_by_altitude(make_aeroplanes(), "9000 - 11000")

    assert [aeroplane.callsign for aeroplane in result] == ["A"]


def test_filter_by_altitude_invalid() -> None:
    """При некорректном диапазоне возвращает исходный список."""
    result = filter_by_altitude(make_aeroplanes(), "abc")

    assert len(result) == 3


def test_sort_by_altitude_desc() -> None:
    """Сортирует по высоте по убыванию."""
    result = sort_by_altitude_desc(make_aeroplanes())

    assert [aeroplane.callsign for aeroplane in result] == ["B", "A", "C"]


def test_get_top() -> None:
    """Возвращает топ-N самолётов."""
    result = get_top(sort_by_altitude_desc(make_aeroplanes()), 2)

    assert [aeroplane.callsign for aeroplane in result] == ["B", "A"]
