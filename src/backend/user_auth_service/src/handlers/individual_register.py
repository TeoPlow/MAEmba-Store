from typing import Any
import requests
from requests.exceptions import RequestException
from schemas.User import User
from core.exceptions import SpecialException
from core.logging import log

def individual_register_handler(data: dict[str, Any]) -> int | SpecialException:
    """
    Регистрирую ФИЗ.ЛИЦо, добавляя его данные в auth_database и в user_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Всё из class User

        Возвращает:
            ID зарегистрированного пользователя, либо SpecialException.
    """
    