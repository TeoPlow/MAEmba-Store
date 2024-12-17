from fastapi import APIRouter, Request
from uuid import UUID

from src.core.logging import log
from src.handlers.get_cart import get_cart_handler
from src.handlers.put_cart_item import put_cart_item_handler
from src.handlers.delete_cart_item import delete_cart_item_handler

router = APIRouter()


@router.get("/{user_id}")
async def get_cart(request: Request, user_id: UUID) -> dict:
    """
    Эндпоинт получения покупок из корзины по ID пользователя.
    """
    log.debug("Получаю информацию о пользователе")
    cart_info: dict = get_cart_handler(user_id)
    return {"status": "success", "data": cart_info}


@router.put("/{user_id}")
async def put_cart_item(request: Request, user_id: UUID) -> dict:
    """
    Эндпоинт добавления/изменения покупок в корзине по ID пользователя.
    """
    log.debug("Получаю информацию о пользователе")
    data = await request.json()
    put_cart_item_handler(data, user_id)
    return {"status": "success"}


@router.delete("/{user_id}")
async def delete_cart_item(request: Request, user_id: UUID) -> dict:
    """
    Эндпоинт удаления покупок из корзины по ID пользователя.
    """
    log.debug("Получаю информацию о пользователе")
    data = await request.json()
    delete_cart_item_handler(data, user_id)
    return {"status": "success"}


