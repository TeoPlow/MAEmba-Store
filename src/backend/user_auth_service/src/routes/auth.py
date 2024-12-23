from fastapi import APIRouter, Request
from uuid import UUID

from src.handlers.validate_auth import validate_auth_handler
from src.handlers.user_register import user_register_handler
from src.handlers.user_login import user_login_handler
from src.core.logging import log

router = APIRouter()


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
            {
             "status": "success",
             "data": {"user_id": eeee1234-76a9-4509-87f0-e1b12354d92b}
            }
    """
    log.debug("Регистрирую пользователя")
    data = await request.json()
    registered_user_id: UUID = user_register_handler(data)
    return {"status": "success", "data": {"user_id": registered_user_id}}


@router.post("/login")
async def login(request: Request):
    """
    Эндпоинт авторизации пользователя.
        На вход:
            Cловарь из email_or_name: (str),
                       password: (str),
                       remember_me: (bool)
                       в формате json.
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
            {
             "status": "success",
             "data": {
                      "token": eeee1234-76a9-4509-87f0-e1b12354d92b,
                      "token-expiry": datetime.timedelta
                     }
            }
    """
    log.debug("Авторизую пользователя")
    data = await request.json()
    token, token_expiry = user_login_handler(data)
    return {"status": "success",
            "data": {"token": token, "token-expiry": token_expiry}}


@router.post("/validate-auth")
async def validate_auth(request: Request):
    """
    """
    log.debug("Проверяю, аутентифицирован ли пользователь")
    try:
        data = await request.json()
        if validate_auth_handler(data):
            return {"status": "success"}
        else:
            return {"status": "warning",
                    "message": "Пользователь не аутентифицирован"}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
