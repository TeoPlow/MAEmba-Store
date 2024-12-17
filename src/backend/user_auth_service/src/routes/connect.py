from fastapi import APIRouter, Request
from uuid import UUID

from src.core.logging import log
from src.core.auth_check import login_required, same_user_required
from src.handlers.get_user_info import get_user_info_handler
from src.handlers.put_user_info import put_user_info_handler

router = APIRouter()


@router.get("/{user_id}")
@login_required
@same_user_required
async def get_user_info(request: Request, user_id: UUID) -> dict:
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
    user_info: dict = get_user_info_handler(user_id)
    return {"status": "success", "data": user_info}


@router.put("/{user_id}")
@login_required
@same_user_required
async def put_user_info(request: Request, user_id: UUID) -> dict:
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
    """
    log.debug("Добавляю информацию о пользователе")
    data = await request.json()
    put_user_info_handler(user_id, data)
    return {"status": "success"}


