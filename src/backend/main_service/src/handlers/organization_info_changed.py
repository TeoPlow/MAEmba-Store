from typing import Any
from core.exceptions import SpecialException

def organization_info_changed_handler(data: dict[str, Any]) -> bool | SpecialException:
    """
    Отправляет запрос к API об изменении информации об аккаунте ЮР.ЛИЦА в user_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                  Только изменяемые данные из class OrganizationProfile

        Возвращает:
            Булевое значение о том, изменена ли информация, либо SpecialException.
    """