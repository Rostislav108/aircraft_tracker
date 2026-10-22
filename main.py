"""Модуль main — взаимодействие с пользователем через консоль."""

from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.filters import filter_by_altitude, filter_by_country, get_top, sort_by_altitude_desc
from src.storage import JSONSaver


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Выводит список самолётов в консоль.

    Args:
        aeroplanes: список самолётов.
    """
    if not aeroplanes:
        print("Самолёты не найдены")
        return
    for index, aeroplane in enumerate(aeroplanes, start=1):
        print(f"{index}. {aeroplane}")


def user_interaction() -> None:
    """Взаимодействует с пользователем через консоль."""
    api = AeroplanesAPI()
    saver = JSONSaver()

    country = input("Введите название страны: ").strip()
    try:
        raw_aeroplanes = api.get_aeroplanes(country)
    except (RuntimeError, ValueError) as error:
        print("Ошибка:", error)
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_aeroplanes)
    print(f"Найдено самолётов над страной {country}: {len(aeroplanes)}")

    try:
        top_n = int(input("Введите количество самолётов для вывода в топ N: "))
    except ValueError:
        top_n = 5
        print("Некорректное число, используется значение по умолчанию: 5")

    filter_words = input("Введите страны для фильтрации по регистрации: ")
    altitude_range = input("Введите диапазон высот (пример: 10000 - 15000): ")

    filtered = filter_by_country(aeroplanes, filter_words)
    ranged = filter_by_altitude(filtered, altitude_range)
    top_aeroplanes = get_top(sort_by_altitude_desc(ranged), top_n)
    print_aeroplanes(top_aeroplanes)

    if top_aeroplanes:
        for aeroplane in top_aeroplanes:
            saver.add_aeroplane(aeroplane)
        print(f"Сохранено в файл: {len(top_aeroplanes)} самолётов")


if __name__ == "__main__":
    user_interaction()
