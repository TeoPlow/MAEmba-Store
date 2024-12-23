import requests
from fastapi import Response, Request
from functools import wraps
from uuid import UUID

from src.core.exceptions import SpecialException
from src.core.config import USER_API_URL
from src.core.logging import log
        
        
def set_cookie(response: Response, name: str, value: str, max_age: int):
    log.debug("Устанавливаю куку")
    # httponly=True, secure=True отвечают за безопасность
    response.set_cookie(key=name, value=value, max_age=max_age, httponly=True, secure=True)

def login_required(f):
    """
    Проверка на то, авторизован ли пользователь.
    """
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        log.debug("Проверка авторизации пользователя")
        data = await request.json()
        url = USER_API_URL + f"/validate-auth"
        headers = {"Content-Type": "application/json"}
        
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['status'] != "success":
            raise SpecialException("Пользователь не авторизован")

        return await f(request, *args, **kwargs)

    return decorated_function

def admin_required(f):
    """
    Проверка на то, является ли пользователь Админом.
    """
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        log.debug("Проверка прав доступа: Админ")
        
        current_user = getattr(request.state, "current_user", None)

        if not current_user:
            log.warning("Пользователь не авторизован")
            raise SpecialException("Вы не авторизованы")

        if current_user.user_role != "Admin":
            log.warning(f"Пользователь {current_user.id} не имеет прав Администратора")
            raise SpecialException("Доступ запрещен: требуется роль Админ")

        return await f(request, *args, **kwargs)

    return decorated_function


def same_user_required(f):
    """
    Проверка на то, совершает ли запрос тот же пользователь, чей ID передаётся в запросе.
    """
    @wraps(f)
    async def decorated_function(request: Request, user_id: UUID, *args, **kwargs):
        log.debug("Проверка доступа: совпадение user_id")

        current_user = getattr(request.state, "current_user", None)

        if not current_user:
            log.warning("Пользователь не авторизован")
            raise SpecialException("Вы не авторизованы")

        if current_user.id != user_id:
            log.warning(f"Доступ запрещен для пользователя {current_user.id} к данным пользователя {user_id}")
            raise SpecialException("Доступ запрещен: несовпадение ID пользователя")

        return await f(request, user_id, *args, **kwargs)

    return decorated_function