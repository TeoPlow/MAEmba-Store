from typing import Any
from fastapi import Depends
import requests
from requests.exceptions import RequestException
from models.User import User
from db.database import get_db_users
from core.exceptions import SpecialException
from core.logging import log
from uuid import UUID

def get_user_info_handler(user_id: UUID, db = Depends(get_db_users)) -> dict[str, Any] | SpecialException:
    """
    Получает информацию о пользователе из user_auth_database.
        Параметры:
            user_id: ID пользователя
                
        Возвращает:
            Словарь с информацией о пользователе или SpecialException.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise SpecialException(f"Пользователь с ID {user_id} не найден.")
        
        user_data = user.to_dict()
        return user_data

    except SpecialException as e:
        log.error(f"Ошибка: {e}")
        return e

    except Exception as e:
        log.error(f"Неизвестная ошибка: {e}")
        raise SpecialException("Произошла неизвестная ошибка при получении информации о пользователе.")