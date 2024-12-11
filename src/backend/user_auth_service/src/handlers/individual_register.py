from typing import Any
from core.exceptions import SpecialException

def individual_registration_handler(data: dict[str, Any]) -> int | SpecialException:
    """
    Выполняет регистрацию физ.лица, добавляя его данные в auth_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Всё из class IndividualProfile

        Возвращает:
            ID зарегистрированного пользователя, либо SpecialException.
    """