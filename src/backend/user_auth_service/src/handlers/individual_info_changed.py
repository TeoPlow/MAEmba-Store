from typing import Any
from core.exceptions import SpecialException

def individual_info_changed_handler(data: dict[str, Any]) -> bool | SpecialException:
    """
    Меняет информацию об аккаунте ФИЗ.ЛИЦА в user_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                  Только изменяемые данные из class IndividualProfile

        Возвращает:
            Булевое значение о том, изменена ли информация, либо SpecialException.
    """