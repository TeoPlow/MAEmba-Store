import requests
from fastapi import APIRouter, Request
from src.core.config import ORDER_API_URL
from src.core.exceptions import SpecialException
from src.core.logging import log

router = APIRouter()


@router.post("/create")
async def create_order(request: Request):
    log.debug("Создаёт новый заказ")
    url = ORDER_API_URL + f"/create"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от ORDER API: {result}")
        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.get("/order={order_id}")
async def get_order_info(order_id: str):
    log.debug("Получаю информацию о заказе")
    url = ORDER_API_URL + f"/order={order_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от ORDER API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.get("/user={user_id}")
async def get_order_info_by_user(user_id: str):
    log.debug("Получаю информацию о заказе по пользователю")
    url = ORDER_API_URL + f"/user={user_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от ORDER API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.put("/update-status")
async def update_status(request: Request):
    log.debug("Обновляет статус заказа")
    url = ORDER_API_URL + f"/update-status"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от ORDER API: {result}")
        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
