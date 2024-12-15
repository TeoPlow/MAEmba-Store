import requests
from requests.exceptions import RequestException

from typing import Any
from uuid import UUID

from src.schemas.User import User
from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.logging import log


def put_user_info_handler(user_id: UUID, data: dict[str, Any]) -> dict | SpecialException:
    """
    Отправляет запрос к API об изменении информации об аккаунте в user_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Только изменяемые данные из class User
        
        Возвращает:
            Словарик с результатом, либо SpecialException.
    """
    log.debug("Изменяю информацию о пользователе пользователя")
    url = USER_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}
    
    try:
        data_check = User.validate_data(data)
        log.debug(f"Получил верные данные: {data_check.print_profile()}")

        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result
    
    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")

