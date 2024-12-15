from fastapi import APIRouter, Request
from uuid import UUID
from src.core.exceptions import SpecialException
from src.core.auth import login_required
from src.core.logging import log
from src.handlers.individual_info_changed import individual_info_changed_handler
from src.handlers.individual_register import individual_register_handler
from src.handlers.organization_info_changed import organization_info_changed_handler
from src.handlers.organization_register import organization_register_handler
from src.handlers.user_login import user_login_handler
from src.handlers.get_user_info import get_user_info_handler

router = APIRouter()

@login_required
@router.post("/change_info")
async def change_info(request: Request):
    log.debug("Меняю информацию об обычном пользователе")
    try:
        data = await request.json()
        is_info_changed: bool = individual_info_changed_handler(data)
        return {"status": "success", "data": is_info_changed}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@login_required
@router.post("/change_info_org")
async def change_info_org(request: Request):
    log.debug("Меняю информацию об организации")
    try:
        data = await request.json()
        is_info_changed: bool = organization_info_changed_handler(data)
        return {"status": "success", "data": is_info_changed}
    except SpecialException as e: 
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    
@router.post("/auth/register")
async def register(request: Request):
    log.debug("Регистрирую обычного пользователя")
    try:
        data = await request.json()
        registered_user_id: UUID = individual_register_handler(data)
        return {"status": "success", "user_id": registered_user_id}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}

@router.post("/auth/register_org")
async def register_org(request: Request):
    log.debug("Регистрирую организацию")
    try:
        data = await request.json()
        registered_org_id: UUID = organization_register_handler(data)
        return {"status": "success", "data": registered_org_id}
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
        put_user_info_handler(user_id)
        return {"status": "success"}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}


