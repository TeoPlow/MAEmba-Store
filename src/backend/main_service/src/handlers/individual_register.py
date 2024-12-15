from typing import Any
import requests
from requests.exceptions import RequestException
from src.schemas.User import User
from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.logging import log

def individual_register_handler(data: dict[str, Any]) -> int | SpecialException:
    """
    Отправляет запрос к API об регистрации ФИЗ.ЛИЦа, добавляя его данные в auth_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Всё из class User

        Возвращает:
            ID зарегистрированного пользователя, либо SpecialException.
    """
    log.debug("Регистрирую обычного пользователя")
    url = USER_API_URL + "auth/register/"
    headers = {"Content-Type": "application/json"}
    
    try:
        if data["user_type"] == 'ind':
            log.debug(f"Получил data: {data}")
            data_check = User.validate_data(data)
            log.debug(f"Получил верные данные: \n{data_check.print_profile()}")
        else:
            raise SpecialException("Переданы данные НЕ пользователя")

        response = requests.post(url, json=data, headers=headers)
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
