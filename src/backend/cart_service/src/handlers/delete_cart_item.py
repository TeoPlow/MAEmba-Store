from uuid import UUID
from typing import Any

from src.models.Cart import Cart
from src.db.database import get_db_cart
from src.core.exceptions import SpecialException
from src.core.logging import log


def delete_cart_item_handler(data: dict[str, Any], user_id: UUID, db=None):
    """
    Удаляет предмет из корзины пользователя по его ID и ID предмета.
        Параметры:
            user_id: ID пользователя
            item_id: ID предмета для удаления
    """
    item_id = data["item_id"]
    log.debug(f"Удаляю предмет {item_id} из корзины пользователя {user_id}")

    if db is None:
        db = next(get_db_cart())

    try:
        result = db.query(Cart).filter(Cart.user_id == user_id, Cart.item_id == item_id).delete()
        
        if result == 0:
            raise SpecialException(f"Запись с user_id={user_id} и item_id={item_id} не найдена в корзине.")

        db.commit()
        log.info(f"Предмет успешно удалён из корзины.")
    finally:
        if db is not None:
            db.close()