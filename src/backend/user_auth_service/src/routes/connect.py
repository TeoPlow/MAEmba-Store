from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from uuid import UUID

from src.core.logging import log
from src.schemas.user_auth_schema import UserDto, UserBase
from src.core.exceptions import SpecialException
from src.handlers.get_user_info import get_user_info_handler
from src.handlers.put_user_info import put_user_info_handler

router = APIRouter()


@router.get("/{user_id}", response_model=UserDto)
async def get_user_info(request: Request, user_id: UUID) -> JSONResponse:
    """
    Эндпоинт получения информации о пользователе по его ID.
    """
    log.debug("Получаю информацию о пользователе")
    try:
        user_info: dict = get_user_info_handler(user_id)
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": user_info}
        )
    except SpecialException as e:
        log.error(f"Ошибка: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )
    except Exception as e:
        log.error(f"Неизвестная ошибка: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error"}
        )


@router.put("/{user_id}")
async def put_user_info(request: UserBase, user_id: UUID) -> JSONResponse:
    """
    Эндпоинт изменения информации о пользователе по его ID.
    """
    log.debug("Обновляю информацию о пользователе")
    try:
        put_user_info_handler(user_id, request.model_dump())
        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Данные обновлены"}
        )
    except SpecialException as e:
        log.error(f"Ошибка: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )
    except Exception as e:
        log.error(f"Неизвестная ошибка: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Беда..."}
        )
