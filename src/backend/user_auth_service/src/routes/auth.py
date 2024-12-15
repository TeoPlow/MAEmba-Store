from fastapi import APIRouter, Request, Response
from uuid import UUID
from src.core.exceptions import SpecialException
from src.core.logging import log
from src.handlers.user_register import user_register_handler
from src.handlers.user_login import user_login_handler

router = APIRouter()

def set_cookie(response: Response, name: str, value: str, max_age: int):
    log.debug("Устанавливаю куку")
    # httponly=True, secure=True отвечают за безопасность
    response.set_cookie(key=name, value=value, max_age=max_age, httponly=True, secure=True)

@router.post("/register")
async def register(request: Request):
    log.debug("Регистрирую пользователя")
    try:
        data = await request.json()
        registered_user_id: UUID = user_register_handler(data)
        return {"status": "success", "data": registered_user_id}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    
@router.post("/login")
async def login(request: Request, response: Response):
    log.debug("Авторизую пользователя")
    try:
        data = await request.json()
        token, token_expiry = user_login_handler(data)
        set_cookie(response, "auth_token", token, max_age=token_expiry.total_seconds())
        return {"status": "success", "token": token}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
