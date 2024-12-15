from typing import Any
import requests
from requests.exceptions import RequestException
from src.schemas.User import User
from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.logging import log

def individual_info_changed_handler(data: dict[str, Any]) -> bool | SpecialException:
    """
    Отправляет запрос к API об изменении информации об аккаунте ФИЗ.ЛИЦА в user_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                user_id и только изменяемые данные из class User

        Возвращает:
            Булевое значение о том, изменена ли информация, либо SpecialException.
    """
    url = USER_API_URL + f"/{data["user_id"]}"
    headers = {"Content-Type": "application/json"}
    
    try:
        data_check = User.validate_data(data)
        log.info(f"Получил верные данные: {data_check.print_profile}")

        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "success" and "user_id" in result:
            log.debug(f"Возвращаю {result["user_id"]}")
            return result["user_id"]
        else:
            raise SpecialException("Неизвестная ошибка")
    
    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")

