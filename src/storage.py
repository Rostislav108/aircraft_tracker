"""Модуль для работы с файлами (хранилище данных о самолётах)."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from src.aeroplane import Aeroplane


class BaseSaver(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолёте в файл."""

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> list[dict[str, Any]]:
        """Возвращает данные о самолётах по указанным критериям."""

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет информацию о самолёте из файла."""


class JSONSaver(BaseSaver):
    """Сохранение информации о самолётах в JSON-файл."""

    def __init__(self, file_path: str | Path = "data/aeroplanes.json") -> None:
        """Инициализирует хранилище.

        Args:
            file_path: путь к JSON-файлу.
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._save([])

    def _load(self) -> list[dict[str, Any]]:
        """Читает список самолётов из файла."""
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        return data if isinstance(data, list) else []

    def _save(self, data: list[dict[str, Any]]) -> None:
        """Записывает список самолётов в файл."""
        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8"
        )

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в JSON-файл.

        Args:
            aeroplane: объект класса Aeroplane.

        Raises:
            TypeError: если передан объект другого класса.
        """
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("Можно добавлять только объекты класса Aeroplane")
        data = self._load()
        data.append(aeroplane.to_dict())
        self._save(data)

    def get_aeroplanes(self, **criteria: Any) -> list[dict[str, Any]]:
        """Возвращает самолёты из файла по критериям.

        Args:
            **criteria: пары «атрибут — значение» для фильтрации,
                например country="Spain".

        Returns:
            Список словарей с данными самолётов.
        """
        data = self._load()
        if not criteria:
            return data
        return [
            item
            for item in data
            if all(item.get(key) == value for key, value in criteria.items())
        ]

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из JSON-файла.

        Args:
            aeroplane: объект класса Aeroplane.

        Raises:
            TypeError: если передан объект другого класса.
        """
        if not isinstance(aeroplane, Aeroplane):
            raise TypeError("Можно удалять только объекты класса Aeroplane")
        target = aeroplane.to_dict()
        data = [item for item in self._load() if item != target]
        self._save(data)
