from functools import wraps
from uuid import UUID
from fastapi import Request
from datetime import datetime

from src.models.Auth import AuthToken
from src.models.User import User
from src.core.exceptions import SpecialException
from src.db.database import get_db_users
from src.core.logging import log

def login_required(f):
    """
    Проверка на то, авторизован ли пользователь.
    """
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        log.debug("Проверка авторизации пользователя")
        token = request.cookies.get("auth_token")

        if not token:
            log.warning("Токен авторизации отсутствует в куках")
            raise SpecialException("Вы не авторизованы")

        with next(get_db_users()) as db:
            auth_token = db.query(AuthToken).filter(AuthToken.token == token).first()
            if not auth_token or auth_token.expires_at < datetime.now():
                log.warning("Токен авторизации недействителен или истёк")
                raise SpecialException("Неверный или истекший токен авторизации")

            request.state.current_user = db.query(User).filter(User.id == auth_token.entity_id).first()
            if not request.state.current_user:
                log.error("Пользователь, связанный с токеном, не найден")
                raise SpecialException("Ошибка аутентификации")

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