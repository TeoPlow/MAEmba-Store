from typing import Any
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from uuid import uuid4
from src.db.database import get_db_users
from src.models.User import User
from src.models.Auth import AuthToken
from src.core.exceptions import SpecialException
from src.core.logging import log

def user_register_handler(data: dict[str, Any], db = None) -> int | SpecialException:
    """
    Регистрирую пользователя, добавляя его данные в user_auth_database.
        Параметры:
            data: Словарь в формате response.json с инфой:
                Всё из class User

        Возвращает:
            ID зарегистрированного пользователя, либо SpecialException.
    """
    log.debug(f"Регистрирую пользователя {data["email"]}")
    if db is None:
        db = next(get_db_users())

    try:
        user = User.validate_data(data)
        log.debug(f"Отвалидировал данные и получил объект пользователя: \n{user.print_profile()}")
        
        log.debug(f"Проверяю, существует ли уже пользователь в БД")
        existing_user = db.query(User).filter(
            (User.email == user.email) | (User.contact_number == user.contact_number)
        ).first()

        if existing_user:
            raise SpecialException(f"Пользователь с email {user.email} или номером {user.contact_number} уже существует.")

        log.debug(f"Добавляю нового пользователя в БД")
        db.add(user)
        db.flush()

        token = AuthToken(
            token=str(uuid4()),
            entity_id=user.id,
            expires_at=datetime.now() + timedelta(days=1),  # Срок действия - 1 день
        )
        log.debug(f"Добавляю токен в БД")
        db.add(token)
        db.commit()

        return user.id

    except IntegrityError as e:
        db.rollback()
        raise SpecialException(f"Ошибка сохранения данных: {e}")

    except ValueError as e:
        db.rollback()
        raise SpecialException(f"Ошибка валидации данных: {e}")
    
    finally:
        if db is not None:
            db.close()