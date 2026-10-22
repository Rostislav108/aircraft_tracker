"""Модуль для работы с API сервисов nominatim и opensky."""

from abc import ABC, abstractmethod
from typing import Any

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPENSKY_URL = "https://opensky-network.org/api/states/all"
USER_AGENT = "aircraft-tracker"


class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервисов."""

    @abstractmethod
    def get_country_bounding_box(self, country: str) -> list[float]:
        """Возвращает координаты страны (юг, север, запад, восток)."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[list[Any]]:
        """Возвращает информацию о самолётах над страной."""


class AeroplanesAPI(BaseAPI):
    """Класс для работы с API nominatim и opensky."""

    def get_country_bounding_box(self, country: str) -> list[float]:
        """Возвращает boundingbox страны.

        Args:
            country: название страны.

        Returns:
            Список координат [юг, север, запад, восток].

        Raises:
            ValueError: если страна не найдена.
            RuntimeError: если запрос к API не удался.
        """
        params: dict[str, Any] = {"country": country, "format": "json", "limit": 1}
        try:
            response = requests.get(
                NOMINATIM_URL,
                params=params,
                headers={"User-Agent": USER_AGENT},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as error:
            raise RuntimeError(
                f"Не удалось получить координаты страны: {error}"
            ) from error

        if not data:
            raise ValueError(f"Страна не найдена: {country}")
        return [float(value) for value in data[0]["boundingbox"]]

    def get_aeroplanes(self, country: str) -> list[list[Any]]:
        """Возвращает данные о самолётах над страной из opensky.

        Args:
            country: название страны.

        Returns:
            Список состояний самолётов (списки значений из API).

        Raises:
            RuntimeError: если запрос к API не удался.
        """
        south, north, west, east = self.get_country_bounding_box(country)
        params: dict[str, float] = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east,
        }
        try:
            response = requests.get(OPENSKY_URL, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as error:
            raise RuntimeError(
                f"Не удалось получить данные о самолётах: {error}"
            ) from error

        states = data.get("states") if isinstance(data, dict) else None
        return states or []
