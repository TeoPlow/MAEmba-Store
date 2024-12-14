from typing import Any
import requests
from requests.exceptions import RequestException
from schemas.User import User
from core.exceptions import SpecialException
from core.config import USER_API_URL
from core.logging import log

def user_login_handler(data: dict[str, Any]) -> bool | SpecialException:
    """
    Выполняет авторизацию пользователя, проверяя наличие вводимых данных в 
    auth_database и устанавливая токен в куку для сохранения авторизации.
        Параметры:
            data: Словарь в формате response.json с инфой:
                  email_or_name: (str)
                  password: (str)
                  remember_me: (bool)

        Возвращает:
            Булевое значение, авторизован ли пользователь, либо SpecialException.
    """