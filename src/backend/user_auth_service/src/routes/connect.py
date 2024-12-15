from fastapi import APIRouter, Request
from uuid import UUID
from src.core.exceptions import SpecialException
from src.core.logging import log
from src.handlers.get_user_info import get_user_info_handler
from src.handlers.put_user_info import put_user_info_handler

router = APIRouter()

@router.get("/{user_id}")
async def get_user_info(user_id: UUID, request: Request):
    log.debug("Получаю информацию о пользователе")
    try:
        user_info: dict = get_user_info_handler(user_id)
        return {"status": "success", "data": user_info}
    except SpecialException as e: 
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@router.put("/{user_id}")
async def put_user_info(user_id: UUID, request: Request):
    log.debug("Добавляю информацию о пользователе")
    try:
        put_user_info_handler(user_id)
        return {"status": "success"}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


