from typing import Any
from src.db.database import get_db_users
from src.models.User import User
from src.core.exceptions import SpecialException
from sqlalchemy.exc import IntegrityError
from src.core.logging import log

def put_user_info_handler(data: dict[str, Any]):
    """
    Обновляет информацию о пользователе в user_database.
        Параметры:
            Словарь с информацией о пользователе.
            
    """
    log.debug("Обновляю информацию о пользователе")
    if db is None:
        db = next(get_db_users())

    try:
        user_id = data.get("id")
        email = data.get("email")

        if not user_id and not email:
            raise SpecialException("Необходимо указать ID или email для идентификации пользователя.")

        user = db.query(User).filter(
            (User.id == user_id) | (User.email == email)
        ).first()

        if not user:
            raise SpecialException(f"Пользователь с ID {user_id} или email {email} не найден.")

        updated_fields = {key: value for key, value in data.items() if hasattr(User, key) and value is not None}

        for key, value in updated_fields.items():
            setattr(user, key, value)

        db.commit()

    except IntegrityError as e:
        db.rollback()
        raise SpecialException(f"Ошибка сохранения данных: {e}")

    except ValueError as e:
        db.rollback()
        raise SpecialException(f"Ошибка валидации данных: {e}")

    finally:
        if db is not None:
            db.close()