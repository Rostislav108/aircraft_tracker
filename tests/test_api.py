"""Тесты модуля api."""

from unittest.mock import Mock, patch

import pytest
import requests

from src.api import AeroplanesAPI


@patch("src.api.requests.get")
def test_get_country_bounding_box(mock_get: Mock) -> None:
    """Возвращает координаты страны из ответа nominatim."""
    mock_response = Mock()
    mock_response.json.return_value = [
        {"boundingbox": ["36.0", "43.79", "-9.5", "4.4"]}
    ]
    mock_get.return_value = mock_response

    result = AeroplanesAPI().get_country_bounding_box("Spain")

    assert result == [36.0, 43.79, -9.5, 4.4]


@patch("src.api.requests.get")
def test_country_not_found(mock_get: Mock) -> None:
    """Если страна не найдена, выбрасывается ValueError."""
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        AeroplanesAPI().get_country_bounding_box("Nowhere")


@patch("src.api.requests.get")
def test_api_error(mock_get: Mock) -> None:
    """Ошибка сети оборачивается в RuntimeError."""
    mock_get.side_effect = requests.RequestException("network")

    with pytest.raises(RuntimeError):
        AeroplanesAPI().get_country_bounding_box("Spain")


@patch("src.api.requests.get")
def test_get_aeroplanes(mock_get: Mock) -> None:
    """Возвращает состояния самолётов из opensky."""
    nominatim = Mock()
    nominatim.json.return_value = [{"boundingbox": ["36.0", "43.79", "-9.5", "4.4"]}]
    opensky = Mock()
    opensky.json.return_value = {
        "states": [["abc", "UAL", "United States", 1, 2, 3, 4, 10000.0, False, 250.0]]
    }
    mock_get.side_effect = [nominatim, opensky]

    states = AeroplanesAPI().get_aeroplanes("Spain")

    assert len(states) == 1
    assert states[0][1] == "UAL"
