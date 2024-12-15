from typing import Any
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from uuid import uuid4
from src.db.database import get_db_users
from src.models.User import User
from src.models.Auth import AuthToken
from src.core.exceptions import SpecialException
from src.core.logging import log


def user_login_handler(data: dict[str, Any], db = None) -> tuple | SpecialException:
    """
    Выполняет авторизацию пользователя, проверяя наличие вводимых данных в 
    auth_database и устанавливая токен в куку для сохранения авторизации.
        Параметры:
            data: Словарь в формате response.json с инфой:
                  email_or_name: (str)
                  password: (str)
                  remember_me: (bool)

        Возвращает:
            Токен авторизации и время авторизации, либо SpecialException.
    """
    log.debug("Авторизация пользователя")
    if db is None:
        db = next(get_db_users())

    try:
        email_or_name = data.get("email_or_name")
        password = data.get("password")
        remember_me = data.get("remember_me", False)

        if not email_or_name or not password:
            raise SpecialException("Необходимо указать email/имя и пароль для авторизации.")

        user = db.query(User).filter(
            (User.email == email_or_name) | (User.username == email_or_name)
        ).first()

        if not user:
            raise SpecialException("Пользователь с указанным email или именем не найден.")

        if not user.check_password(password):
            raise SpecialException("Неверный пароль.")

        # Создание токена авторизации
        token_expiry = timedelta(days=30) if remember_me else timedelta(hours=12)
        token = AuthToken(
            token=str(uuid4()),
            entity_id=user.id,
            expires_at=datetime.now() + token_expiry,
        )
        db.add(token)
        db.commit()

        log.info(f"Пользователь {user.id} успешно авторизован.")
        return token.token, token_expiry

    except IntegrityError as e:
        db.rollback()
        raise SpecialException(f"Ошибка сохранения данных: {e}")

    except ValueError as e:
        db.rollback()
        raise SpecialException(f"Ошибка валидации данных: {e}")

    finally:
        if db is not None:
            db.close()