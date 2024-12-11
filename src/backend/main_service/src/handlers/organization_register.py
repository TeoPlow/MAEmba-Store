from typing import Any
import requests
from requests.exceptions import RequestException
from schemas.OrganizationProfile import OrganizationProfile
from core.exceptions import SpecialException
from core.config import USER_API_URL
from core.logging import logger_config, log
import logging.config

logging.config.dictConfig(logger_config)

def organization_register_handler(data: dict[str, Any]) -> int | SpecialException:
    """
    Отправляет запрос к API об регистрации ЮР.ЛИЦа, добавляя его данные в auth_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Всё из class OrganizationProfile

        Возвращает:
            ID зарегистрированного пользователя, либо SpecialException.
    """
    url = USER_API_URL + "auth/register-org/"
    headers = {"Content-Type": "application/json"}
    
    try:
        data_check = OrganizationProfile.validate_data(data)
        log.debug(f"Получил верные данные: {data_check.print_profile}")

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

