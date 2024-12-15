from fastapi import APIRouter, Request
from uuid import UUID

from src.core.exceptions import SpecialException
from src.core.auth import login_required, admin_required, same_user_required
from src.core.logging import log

from src.handlers.user_register import user_register_handler
from src.handlers.user_login import user_login_handler
from src.handlers.get_user_info import get_user_info_handler
from src.handlers.put_user_info import put_user_info_handler

router = APIRouter()

@router.post("/auth/register")
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
        return {"status": "success", "user_id": registered_user_id}
    except SpecialException as e:
        log.warning(e)
        return {"status": "warning", "message": str(e)}
    except Exception as e:
        log.error(f'Ошибка: {e}')
        return {"status": "error", "message": str(e)}
    
@router.post("/auth/login")
async def login(request: Request):
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
    log.debug("Авторизую уже существующего пользователя")
    try:
        data = await request.json()
        token: UUID = user_login_handler(data)
        return {"status": "success", "token": token}
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
async def get_user_info(user_id: UUID):
    """
    Эндпоинт получения информации о пользователе по его ID.
        На вход:
            Внутри эндпоинта '/user_id'
            Пример:
                http://0.0.0.0:8000/user/e5f8433e-76a9-4509-87f0-e1b12354d92b

        Возвращает:
            Cловарь из class User в формате json, но без пароля.
            Пример:
                {
                "status":"success",
                "data":{
                    "id":"e5f8433e-76a9-4509-87f0-e1b12354d92b",
                    "email":"AGUREZ@yandex.com",
                    "user_type":"ind",
                    "username":"egor228",
                    "contact_number":"+79853553825",
                    "user_role":"Not_Verifyed",
                    "created":"2024-12-15T15:48:46.195517+03:00",
                    "updated":"2024-12-15T21:01:34.382072+03:00"
                    }
                }
    """
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
    """
    Эндпоинт изменения информации о пользователе по его ID.
        На вход:
            Внутри эндпоинта '/user_id', а также словарь из class User в формате json.
            Пример:
                http://0.0.0.0:8000/user/e5f8433e-76a9-4509-87f0-e1b12354d92b

                "Content-Type: application/json"
                {
                "user_type": "ind", 
                "username": "new_egor228", 
                "password": "new_password", 
                "email": "new_citymodz@yandex.com", 
                "contact_number": "+79000111222"
                }'

        Возвращает:
            Cловарь из class User в формате json, но без пароля.
            Пример:
                {
                "status":"success",
                "data":{
                    "id":"e5f8433e-76a9-4509-87f0-e1b12354d92b",
                    "email":"AGUREZ@yandex.com",
                    "user_type":"ind",
                    "username":"egor228",
                    "contact_number":"+79853553825",
                    "user_role":"Not_Verifyed",
                    "created":"2024-12-15T15:48:46.195517+03:00",
                    "updated":"2024-12-15T21:01:34.382072+03:00"
                    }
                }
    """
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


