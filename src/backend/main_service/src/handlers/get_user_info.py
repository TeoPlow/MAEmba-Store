from typing import Any
import requests
from requests.exceptions import RequestException
from src.schemas.User import User
from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.logging import log
from uuid import UUID

def get_user_info_handler(user_id: UUID) -> dict[str, Any] | SpecialException:
    """
    Получает информацию о пользователе из User_Auth API.
        Параметры:
            user_id: ID пользователя
                
        Возвращает:
            Словарь типа class User.
    """
    url = USER_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от USER API: {result}")
        
        if result["status"] == "success":
            log.debug(f"Возвращаю инфу о {result["data"]["email"]}")
            return result["data"]
        else:
            raise SpecialException("Передача прошла не успешно")
    
    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")