from typing import Any
from src.models.User import User
from src.db.database import get_db_users
from src.core.exceptions import SpecialException
from src.core.logging import log
from uuid import UUID

def get_user_info_handler(user_id: UUID, db = None) -> dict[str, Any] | SpecialException:
    """
    Получает информацию о пользователе из user_auth_database.
        Параметры:
            user_id: ID пользователя
                
        Возвращает:
            Словарь с информацией о пользователе или SpecialException.
    """
    log.debug("Получаю информацию о пользователе")
    if db is None:
        db = next(get_db_users())

    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise SpecialException(f"Пользователь с ID {user_id} не найден.")
        
        user_data = user.to_dict()
        return user_data
    finally:
        if db is not None:
            db.close()