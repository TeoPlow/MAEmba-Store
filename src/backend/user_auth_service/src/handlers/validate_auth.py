from fastapi import Response, Request
from functools import wraps
from uuid import UUID
from datetime import datetime

from src.models.Auth import AuthToken
from src.models.User import User
from src.core.exceptions import SpecialException
from src.db.database import get_db_users
from src.core.logging import log


def validate_auth_handler(request: Request):
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