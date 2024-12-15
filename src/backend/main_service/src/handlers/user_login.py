from typing import Any
import requests
from requests.exceptions import RequestException
from src.schemas.User import User
from uuid import UUID
from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.logging import log

def user_login_handler(data: dict[str, Any]) -> UUID | SpecialException:
    """
    Выполняет авторизацию пользователя, проверяя наличие вводимых данных в 
    auth_database и устанавливая токен в куку для сохранения авторизации.
        Параметры:
            data: Словарь в формате response.json с инфой:
                  email_or_name: (str)
                  password: (str)
                  remember_me: (bool)

        Возвращает:
            Токен авторизации, либо SpecialException.
    """
    url = USER_API_URL + "/auth/login/"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "success" and "token" in result:
            log.debug(f"Возвращаю {result["token"]}")
            return result["token"]
        else:
            raise SpecialException("Неизвестная ошибка")
    
    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")