import requests
from requests.exceptions import RequestException
from fastapi import APIRouter, Request
from uuid import UUID

from src.core.config import CART_API_URL
from src.core.exceptions import SpecialException
from src.core.logging import log


router = APIRouter()


@router.get("/{user_id}")
async def get_cart(user_id: UUID):
    """
    Получает информацию о корзине из Cart API.
        Параметры:
            user_id: ID пользователя

        Возвращает:
            Словарь типа class Cart.
    """
    url = CART_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от CART API: {result}")

        if result["status"] == "success":
            return result["data"]
        if result["status"] == "warning":
            return result["message"]
        else:
            raise SpecialException("Передача прошла не успешно")

    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")


@router.post("/{user_id}")
async def put_cart_item(request: Request, user_id: UUID):
    """
    Отправляет запрос на добавление предмета в Cart API.
        Параметры:
            user_id: ID пользователя

        Возвращает:
            Словарь типа class Cart.
    """
    url = CART_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от CART API: {result}")

        if result["status"] == "success":
            return result["data"]
        if result["status"] == "warning":
            return result["message"]
        else:
            raise SpecialException("Передача прошла не успешно")

    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")


@router.delete("/{user_id}")
async def delete_cart_item(request: Request, user_id: UUID):
    """
    Удаляет предмет в Cart API.
        Параметры:
            user_id: ID пользователя

        Возвращает:
            Словарь типа class Cart.
    """
    url = CART_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.delete(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от CART API: {result}")

        if result["status"] == "success":
            return result["data"]
        if result["status"] == "warning":
            return result["message"]
        else:
            raise SpecialException("Передача прошла не успешно")

    except RequestException as e:
        raise SpecialException(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        raise SpecialException(f"Ошибка обработки ответа: {e}")
