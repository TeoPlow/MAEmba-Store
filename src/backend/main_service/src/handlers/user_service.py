import requests
from requests.exceptions import RequestException

from typing import Any
from uuid import UUID

from src.schemas.User import User
from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.config import RECAPTCHA_KEY
from src.core.logging import log
from src.core.auth import set_cookie, verify_recaptcha
# from src.core.auth import login_required, admin_required, same_user_required


def user_login_handler(data: dict[str, Any]):
    """
    Выполняет авторизацию пользователя, проверяя наличие вводимых данных в
    auth_database и устанавливая токен в куку для сохранения авторизации.
        Параметры:
            data: Словарь в формате response.json с инфой:
                  email_or_name: (str)
                  password: (str)
                  remember_me: (bool)
                  captcha_token: (str) - токен капчи
    """
    log.debug("Авторизую пользователя")
    url = USER_API_URL + "/auth/login/"
    headers = {"Content-Type": "application/json"}

    try:
        if not verify_recaptcha(data["captcha_token"], RECAPTCHA_KEY):
            raise SpecialException("Капча не пройдена")

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "success":
            token = result["data"]["token"]
            token_expiry = result["data"]["token-expiry"]

            set_cookie(response,
                       "auth_token",
                       token,
                       max_age=token_expiry.total_seconds())
            log.debug(f"Установил ТОКЕН в куку: {token} на {token_expiry}")

        else:
            raise SpecialException(f"Ошибка при получении ответа: {result}")

    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")


def user_register_handler(data: dict[str, Any]) -> int | SpecialException:
    """
    Отправляет запрос к API об регистрации аккаунта,
    добавляя его данные в auth_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Всё из class User

        Возвращает:
            ID зарегистрированного пользователя, либо SpecialException.
    """
    log.debug("Регистрирую пользователя")
    url = USER_API_URL + "auth/register/"
    headers = {"Content-Type": "application/json"}

    try:
        if data["user_type"] == 'ind':
            log.debug(f"Получил data: {data}")
            data_check = User.validate_data(data)
            log.debug(f"Получил верные данные: \n{data_check.print_profile()}")
        else:
            raise SpecialException("Переданные данные НЕ ВЕРНЫЕ")

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил в POST запросе {result}")
        if result['status'] == "success":
            log.debug(f"Возвращаю user_id: {result["data"]["user_id"]}")
            return result["data"]["user_id"]
        else:
            raise SpecialException(f"Что-то случилось в USER API: {result}")

    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")


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
        if result["status"] == "warning":
            return result["message"]
        else:
            raise SpecialException("Передача прошла не успешно")

    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")


def put_user_info_handler(user_id: UUID,
                          data: dict[str, Any]) -> dict | SpecialException:
    """
    Отправляет запрос к USER API об изменении информации
    об аккаунте в user_database.
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


def validate_auth_handler(data: dict[str, Any]) -> dict | SpecialException:
    """
    Отправляет запрос к USER API об проверке,
    является ли аккаунт аутентифицированным в user_auth_database.
        Параметры:
            data: Словарь в формате response.json

        Возвращает:
            Словарик с результатом, либо SpecialException.
    """
    log.debug("Проверяю, является ли аккаунт аутентифицированным")
    url = USER_API_URL + "/validate-auth"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result

    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")
