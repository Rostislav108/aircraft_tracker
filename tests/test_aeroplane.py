"""Тесты класса Aeroplane."""

import pytest

from src.aeroplane import Aeroplane


def test_aeroplane_init() -> None:
    """Проверяет инициализацию самолёта."""
    aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)

    assert aeroplane.callsign == "UAL1621"
    assert aeroplane.country == "United States"
    assert aeroplane.velocity == 268.79
    assert aeroplane.altitude == 10203.18


def test_invalid_callsign() -> None:
    """Пустой позывной недопустим."""
    with pytest.raises(ValueError):
        Aeroplane("", "Spain", 100.0, 1000.0)


def test_invalid_velocity() -> None:
    """Скорость должна быть числом."""
    with pytest.raises(ValueError):
        Aeroplane("UAL", "Spain", "abc", 1000.0)


def test_negative_altitude() -> None:
    """Высота не может быть отрицательной."""
    with pytest.raises(ValueError):
        Aeroplane("UAL", "Spain", 100.0, -5.0)


def test_cast_to_object_list() -> None:
    """Преобразует данные opensky в объекты и пропускает некорректные."""
    raw = [
        ["abc", "UAL1621", "United States", None, None, None, None, 10203.18, None, 268.79],
        ["def", None, None, None, None, None, None, None, None, None],
    ]

    aeroplanes = Aeroplane.cast_to_object_list(raw)

    assert len(aeroplanes) == 1
    assert aeroplanes[0].callsign == "UAL1621"


def test_comparison_by_speed_and_altitude() -> None:
    """Самолёты сравниваются по скорости и высоте."""
    fast = Aeroplane("A", "Spain", 300.0, 9000.0)
    slow = Aeroplane("B", "Spain", 100.0, 10000.0)

    assert fast.is_faster_than(slow)
    assert slow.is_higher_than(fast)
    assert fast > slow


def test_equality() -> None:
    """Самолёты равны при одинаковых скорости и высоте."""
    first = Aeroplane("A", "Spain", 250.0, 10000.0)
    second = Aeroplane("B", "France", 250.0, 10000.0)

    assert first == second


def test_to_dict() -> None:
    """Словарь содержит все атрибуты самолёта."""
    aeroplane = Aeroplane("UAL", "Spain", 100.0, 1000.0)

    assert aeroplane.to_dict() == {
        "callsign": "UAL",
        "country": "Spain",
        "velocity": 100.0,
        "altitude": 1000.0,
    }
