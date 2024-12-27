import requests
from fastapi import APIRouter, Request
from uuid import UUID

from src.core.config import CART_API_URL
from src.core.exceptions import SpecialException
from src.core.logging import log


router = APIRouter()


@router.get("/{user_id}")
async def get_cart(user_id: UUID):
    url = CART_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от CART API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@router.put("/{user_id}")
async def put_cart_item(request: Request, user_id: UUID):
    url = CART_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от CART API: {result}")
        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.delete("/{user_id}")
async def delete_cart_item(request: Request, user_id: UUID):
    url = CART_API_URL + f"/{user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.delete(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от CART API: {result}")
        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
