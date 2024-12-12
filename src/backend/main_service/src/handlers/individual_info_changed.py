from typing import Any
from core.exceptions import SpecialException

def individual_info_changed_handler(data: dict[str, Any]) -> bool | SpecialException:
    """
    Отправляет запрос к API об изменении информации об аккаунте ФИЗ.ЛИЦА в user_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                user_id и только изменяемые данные из class IndividualProfile

        Возвращает:
            Булевое значение о том, изменена ли информация, либо SpecialException.
    """
