from typing import Any, List
from uuid import UUID

from src.models.Cart import Cart
from src.db.database import get_db_cart
from src.core.exceptions import SpecialException
from src.core.logging import log


def get_cart_handler(user_id: UUID, db = None) -> dict[str, Any] | SpecialException:
    """
    Получает информацию о корзине из cart_database.
        Параметры:
            user_id: ID пользователя
                
        Возвращает:
            Словарь с информацией о корзине или SpecialException.
    """
    log.debug("Получаю информацию о корзине")
    if db is None:
        db = next(get_db_cart())

    try:
        cart: List[Cart] = db.query(Cart).filter(Cart.user_id == user_id).all()
        
        if not cart:
            raise SpecialException(f"Корзина пользователя с ID {user_id} не найдена.")
        
        cart_data = []
        for item in cart:
            cart_data.append(item.to_dict())

        return cart_data
    finally:
        if db is not None:
            db.close()