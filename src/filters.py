"""Модуль с функциями фильтрации и сортировки самолётов."""

from src.aeroplane import Aeroplane


def filter_by_country(
    aeroplanes: list[Aeroplane], countries: str
) -> list[Aeroplane]:
    """Фильтрует самолёты по стране регистрации.

    Args:
        aeroplanes: список самолётов.
        countries: названия стран через запятую.

    Returns:
        Список самолётов, зарегистрированных в указанных странах.
    """
    names = [name.strip().lower() for name in countries.split(",") if name.strip()]
    if not names:
        return list(aeroplanes)
    return [aeroplane for aeroplane in aeroplanes if aeroplane.country.lower() in names]


def filter_by_altitude(
    aeroplanes: list[Aeroplane], altitude_range: str
) -> list[Aeroplane]:
    """Фильтрует самолёты по диапазону высот.

    Args:
        aeroplanes: список самолётов.
        altitude_range: диапазон в виде «10000 - 15000».

    Returns:
        Самолёты, высота которых попадает в диапазон.
        При некорректном диапазоне возвращается исходный список.
    """
    try:
        low_raw, high_raw = altitude_range.split("-")
        low, high = float(low_raw.strip()), float(high_raw.strip())
    except (ValueError, AttributeError):
        print("Некорректный диапазон высот. Пример: 10000 - 15000")
        return list(aeroplanes)
    if low > high:
        low, high = high, low
    return [aeroplane for aeroplane in aeroplanes if low <= aeroplane.altitude <= high]


def sort_by_altitude_desc(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортирует самолёты по высоте по убыванию.

    Args:
        aeroplanes: список самолётов.

    Returns:
        Новый список, отсортированный по высоте от большей к меньшей.
    """
    return sorted(aeroplanes, key=lambda aeroplane: aeroplane.altitude, reverse=True)


def get_top(aeroplanes: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    """Возвращает первые N самолётов списка.

    Args:
        aeroplanes: список самолётов.
        top_n: количество самолётов для вывода.

    Returns:
        Список не длиннее top_n.
    """
    return list(aeroplanes[: max(top_n, 0)])
