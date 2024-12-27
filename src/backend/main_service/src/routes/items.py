import requests
from fastapi import APIRouter, Request
from src.core.config import ITEMS_API_URL
from uuid import UUID
from src.core.exceptions import SpecialException
from src.core.logging import log

router = APIRouter()


@router.get("/item/{item_id}")
async def get_item(item_id: UUID):
    log.debug("Получаю информацию о товаре")
    url = ITEMS_API_URL + f"/item/{item_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от ITEMS API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


@router.get("/item/search")
async def search_items(item_id: UUID):
    log.debug("Поиск товара по параметрам")
    url = ITEMS_API_URL + f"/item/search"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от ITEMS API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.put("/item")
async def put_item(request: Request):
    log.debug("Обновление информации о товаре")
    url = ITEMS_API_URL + f"/item"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от ITEMS API: {result}")
        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.post("/item")
async def post_item(request: Request):
    log.debug("Создаёт товар")
    url = ITEMS_API_URL + f"/item"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от ITEMS API: {result}")
        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.get("/category/{category_id}")
async def get_category(category_id: str):
    log.debug("Получение названия категории")
    url = ITEMS_API_URL + f"/category/{category_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от ITEMS API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.get("/category")
async def get_category():
    log.debug("Получение всех категорий")
    url = ITEMS_API_URL + f"/category"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от ITEMS API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.post("/category")
async def post_category(request: Request):
    log.debug("Добавление категории")
    url = ITEMS_API_URL + f"/category"
    headers = {"Content-Type": "application/json"}

    try:
        data = await request.json()
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        log.debug(f"Получил от ITEMS API: {result}")
        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    

@router.get("/item/page={page_num}&page_size={page_size}")
async def search_items(page_num: str, page_size: str):
    log.debug("Поиск товара по параметрам")
    url = ITEMS_API_URL + f"/item/page={page_num}&page_size={page_size}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        log.debug(f"Получил от ITEMS API: {result}")

        return result

    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}