from fastapi import Request
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
        query = db.query(AuthToken).filter(AuthToken.token == token)
        auth_token = query.first()
        if not auth_token or auth_token.expires_at < datetime.now():
            log.warning("Токен авторизации недействителен или истёк")
            raise SpecialException("Неверный или истекший токен авторизации")

        query = db.query(User).filter(User.id == auth_token.entity_id)
        request.state.current_user = query.first()
        if not request.state.current_user:
            log.error("Пользователь, связанный с токеном, не найден")
            raise SpecialException("Ошибка аутентификации")
