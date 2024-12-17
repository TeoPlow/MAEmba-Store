import requests
from fastapi import Response
from requests.exceptions import RequestException

from typing import Any
from uuid import UUID

from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.logging import log


def set_cookie(response: Response, name: str, value: str, max_age: int):
    log.debug("Устанавливаю куку")
    # httponly=True, secure=True отвечают за безопасность
    response.set_cookie(key=name, value=value, max_age=max_age, httponly=True, secure=True)
    

def user_login_handler(data: dict[str, Any]):
    """
    Выполняет авторизацию пользователя, проверяя наличие вводимых данных в 
    auth_database и устанавливая токен в куку для сохранения авторизации.
        Параметры:
            data: Словарь в формате response.json с инфой:
                  email_or_name: (str)
                  password: (str)
                  remember_me: (bool)
    """
    log.debug("Авторизую пользователя")
    url = USER_API_URL + "/auth/login/"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "success" and "token" in result:
            token, token_expiry = result["token"], result["token-expiry"]

            set_cookie(response, "auth_token", token, max_age=token_expiry.total_seconds())
            log.debug(f"Установил ТОКЕН в куку: {token} на время {token_expiry}")

        else:
            raise SpecialException(f"Неизвестная ошибка {result}")
    
    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")