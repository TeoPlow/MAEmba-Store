from fastapi import APIRouter, Request
from uuid import UUID
from src.core.exceptions import SpecialException
from src.core.auth import login_required
from src.core.logging import log
from src.handlers.user_register import user_register_handler
from src.handlers.user_login import user_login_handler
from src.handlers.get_user_info import get_user_info_handler
from src.handlers.put_user_info import put_user_info_handler

router = APIRouter()

@router.post("/auth/register")
async def register(request: Request):
    log.debug("Регистрирую пользователя")
    try:
        data = await request.json()
        registered_user_id: UUID = user_register_handler(data)
        return {"status": "success", "user_id": registered_user_id}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    
@router.post("/auth/login")
async def login(request: Request):
    log.debug("Авторизую уже существующего пользователя")
    try:
        data = await request.json()
        token: UUID = user_login_handler(data)
        return {"status": "success", "data": token}
    except SpecialException as e: 
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@router.post("/auth/validate-token")
async def validate_token(request: Request):
    pass

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
        data = await request.json()
        result: dict = put_user_info_handler(user_id, data)
        return {"status": "success"}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


