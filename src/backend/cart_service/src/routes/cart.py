from fastapi import APIRouter, Request
from uuid import UUID
from http import HTTPStatus
from fastapi.responses import JSONResponse

from src.core.logging import log
from src.core.exceptions import SpecialException
from src.handlers.get_cart import get_cart_handler
from src.handlers.put_cart_item import put_cart_item_handler
from src.handlers.delete_cart_item import delete_cart_item_handler

from src.schemas.cart_schema import (
    # CartItem,
    GetCartResponse,
    UpdateCartRequest,
    UpdateCartResponse,
    DeleteCartItemRequest,
    DeleteCartItemResponse
)

router = APIRouter()


@router.get("/{user_id}",
            response_model=GetCartResponse,
            description="Получение корзины по ID пользователя")
async def get_cart(request: Request, user_id: UUID) -> GetCartResponse:
    """
    Эндпоинт получения покупок из корзины по ID пользователя.
    """
    log.debug("Получаю информацию о пользователе")
    try:
        cart_info = get_cart_handler(user_id)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"status": "success", "data": cart_info}
        )
    except SpecialException as e:
        log.warning(f"Ошибка: {e}")
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        log.error(f"Ошибка: {e}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@router.put("/{user_id}",
            response_model=UpdateCartResponse,
            description="Добавление/изменение товаров в корзине по ID")
async def put_cart_item(request: UpdateCartRequest,
                        user_id: UUID) -> UpdateCartResponse:
    """
    Эндпоинт добавления/изменения покупок в корзине по ID пользователя.
    """
    log.debug("Получаю информацию о пользователе")
    try:
        put_cart_item_handler(request.model_dump(), user_id)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"status": "success"}
        )
    except SpecialException as e:
        log.warning(f"Ошибка: {e}")
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        log.error(f"Ошибка: {e}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@router.delete("/{user_id}",
               response_model=DeleteCartItemResponse,
               description="Удаление товара из корзины по ID пользователя")
async def delete_cart_item(request: DeleteCartItemRequest,
                           user_id: UUID) -> DeleteCartItemResponse:
    """
    Эндпоинт удаления покупок из корзины по ID пользователя.
    """
    log.debug("Получаю информацию о пользователе")
    try:
        delete_cart_item_handler(request.model_dump(), user_id)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"status": "success"}
        )
    except SpecialException as e:
        log.warning(f"Ошибка: {e}")
        return JSONResponse(
            content={"status": "warning", "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        log.error(f"Ошибка: {e}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
