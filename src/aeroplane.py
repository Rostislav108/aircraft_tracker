"""Модуль с классом Aeroplane (самолёт)."""

from typing import Any


class Aeroplane:
    """Самолёт с информацией о полёте.

    Attributes:
        callsign: позывной самолёта.
        country: страна регистрации.
        velocity: скорость полёта, м/с.
        altitude: высота полёта, м.
    """

    def __init__(
        self, callsign: str, country: str, velocity: float, altitude: float
    ) -> None:
        """Инициализирует самолёт с валидацией данных.

        Args:
            callsign: позывной самолёта.
            country: страна регистрации.
            velocity: скорость полёта в м/с.
            altitude: высота полёта в метрах.

        Raises:
            ValueError: если данные некорректны.
        """
        self.callsign = self._validate_text(callsign, "Позывной")
        self.country = self._validate_text(country, "Страна регистрации")
        self.velocity = self._validate_number(velocity, "Скорость")
        self.altitude = self._validate_number(altitude, "Высота")

    @staticmethod
    def _validate_text(value: Any, name: str) -> str:
        """Проверяет, что значение — непустая строка."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} должен быть непустой строкой")
        return value.strip()

    @staticmethod
    def _validate_number(value: Any, name: str) -> float:
        """Проверяет, что значение — неотрицательное число."""
        try:
            number = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{name} должен быть числом") from error
        if number < 0:
            raise ValueError(f"{name} не может быть отрицательным")
        return number

    @classmethod
    def cast_to_object_list(cls, raw_aeroplanes: list[list[Any]]) -> list["Aeroplane"]:
        """Преобразует данные opensky в список объектов Aeroplane.

        Args:
            raw_aeroplanes: список состояний самолётов из API.

        Returns:
            Список объектов Aeroplane. Некорректные записи пропускаются.
        """
        aeroplanes = []
        for state in raw_aeroplanes:
            try:
                callsign = state[1] or "Неизвестно"
                country = state[2] or "Неизвестно"
                altitude = state[7] if state[7] is not None else state[13]
                velocity = state[9]
                if altitude is None or velocity is None:
                    continue
                aeroplanes.append(cls(callsign, country, velocity, altitude))
            except (ValueError, IndexError, TypeError):
                continue
        return aeroplanes

    def is_faster_than(self, other: "Aeroplane") -> bool:
        """Сравнивает самолёты по скорости."""
        return self.velocity > other.velocity

    def is_higher_than(self, other: "Aeroplane") -> bool:
        """Сравнивает самолёты по высоте полёта."""
        return self.altitude > other.altitude

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.velocity, self.altitude) == (other.velocity, other.altitude)

    def __lt__(self, other: "Aeroplane") -> bool:
        return (self.velocity, self.altitude) < (other.velocity, other.altitude)

    def __le__(self, other: "Aeroplane") -> bool:
        return (self.velocity, self.altitude) <= (other.velocity, other.altitude)

    def __gt__(self, other: "Aeroplane") -> bool:
        return (self.velocity, self.altitude) > (other.velocity, other.altitude)

    def __ge__(self, other: "Aeroplane") -> bool:
        return (self.velocity, self.altitude) >= (other.velocity, other.altitude)

    def to_dict(self) -> dict[str, Any]:
        """Возвращает данные самолёта в виде словаря."""
        return {
            "callsign": self.callsign,
            "country": self.country,
            "velocity": self.velocity,
            "altitude": self.altitude,
        }

    def __str__(self) -> str:
        return (
            f"{self.callsign} ({self.country}): "
            f"скорость {self.velocity} м/с, высота {self.altitude} м"
        )
