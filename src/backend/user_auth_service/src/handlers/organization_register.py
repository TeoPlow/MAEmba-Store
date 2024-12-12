from typing import Any
from core.exceptions import SpecialException

def organization_register_handler(data: dict[str, Any]) -> int | SpecialException:
    """
    Выполняет регистрацию юр.лица, добавляя его данные в auth_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Всё из class OrganizationProfile

        Возвращает:
            ID зарегистрированного пользователя, либо SpecialException.
    """