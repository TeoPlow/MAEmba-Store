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
    """
    Эндпоинт регистрации пользователя.
        На вход:
            Cловарь из class User в формате json.
            Пример:
                "Content-Type: application/json"
                {
                "user_type": "ind", 
                "username": "egor228", 
                "password": "password", 
                "email": "citymodz@yandex.com", 
                "contact_number": "+79853553825"
                }
                
        Возвращает:
            UUID зарегестрированного пользователя
            Пример:
            {"status": "success", "user_id": eeee1234-76a9-4509-87f0-e1b12354d92b}
    """
    log.debug("Регистрирую пользователя")
    try:
        data = await request.json()
        registered_user_id: UUID = user_register_handler(data)
        log.debug(f"Регистрация успешно окончена")
        return {"status": "success", "user_id": registered_user_id}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    
@router.post("/login")
async def login(request: Request, response: Response):
    """
    Эндпоинт авторизации пользователя.
        На вход:
            Cловарь из email_or_name: (str), password: (str), remember_me: (bool) в формате json.
            Пример:
                "Content-Type: application/json"
                {
                "email_or_name": "username",
                "password": "pass12345",
                "remember_me": True
                }

        Возвращает:
            UUID Токен авторизации по ключу "token"
            Пример:
            {"status": "success", "token": eeee1234-76a9-4509-87f0-e1b12354d92b}
    """
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
