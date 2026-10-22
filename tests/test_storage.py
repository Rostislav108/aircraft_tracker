"""Тесты класса JSONSaver."""

import pytest

from src.aeroplane import Aeroplane
from src.storage import JSONSaver


def test_add_and_get(tmp_path) -> None:
    """Добавляет самолёт и возвращает его из файла."""
    saver = JSONSaver(tmp_path / "aeroplanes.json")

    saver.add_aeroplane(Aeroplane("UAL", "Spain", 250.0, 10000.0))

    data = saver.get_aeroplanes()
    assert len(data) == 1
    assert data[0]["callsign"] == "UAL"


def test_get_with_criteria(tmp_path) -> None:
    """Возвращает самолёты по критериям."""
    saver = JSONSaver(tmp_path / "aeroplanes.json")
    saver.add_aeroplane(Aeroplane("A", "Spain", 250.0, 10000.0))
    saver.add_aeroplane(Aeroplane("B", "France", 260.0, 11000.0))

    result = saver.get_aeroplanes(country="Spain")

    assert len(result) == 1
    assert result[0]["callsign"] == "A"


def test_delete(tmp_path) -> None:
    """Удаляет самолёт из файла."""
    saver = JSONSaver(tmp_path / "aeroplanes.json")
    first = Aeroplane("A", "Spain", 250.0, 10000.0)
    second = Aeroplane("B", "France", 260.0, 11000.0)
    saver.add_aeroplane(first)
    saver.add_aeroplane(second)

    saver.delete_aeroplane(first)

    data = saver.get_aeroplanes()
    assert len(data) == 1
    assert data[0]["callsign"] == "B"


def test_invalid_json(tmp_path) -> None:
    """Повреждённый JSON обрабатывается без ошибок."""
    path = tmp_path / "aeroplanes.json"
    path.write_text("not json", encoding="utf-8")
    saver = JSONSaver(path)

    assert saver.get_aeroplanes() == []


def test_add_invalid_type(tmp_path) -> None:
    """Нельзя добавить объект другого класса."""
    saver = JSONSaver(tmp_path / "aeroplanes.json")

    with pytest.raises(TypeError):
        saver.add_aeroplane("не самолёт")
