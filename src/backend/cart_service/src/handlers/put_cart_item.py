from uuid import UUID
from typing import Any

from src.models.Cart import Cart
from src.db.database import get_db_cart
from src.core.logging import log


def put_cart_item_handler(data: dict[str, Any], user_id: UUID, db=None):
    """
    Добавляет товар в корзину пользователя или обновляет его количество.
        Параметры:
            user_id: ID пользователя
    """

    if db is None:
        db = next(get_db_cart())

    try:
        item_id = data["item_id"]
        quantity = data["quantity"]
        price = data["price"]
        log.debug(f"Обновляю {item_id}, ценой {price} для {user_id}")

        cart_item = db.query(Cart).filter(Cart.user_id == user_id,
                                          Cart.item_id == item_id).first()

        sum_price = round(price * quantity, 2)

        if cart_item:
            log.debug(f"Товар {item_id} уже в корзине. Обновляю кол-во и цену")
            cart_item.quantity = quantity
            cart_item.price = sum_price
        else:
            log.debug(f"Товар {item_id} отсутствует в корзине. Добавляю товар")
            new_cart_item = Cart(user_id, item_id, quantity, price=sum_price)
            db.add(new_cart_item)

        db.commit()
        log.debug(f"Товар {item_id} успешно добавлен/обновлён для {user_id}")
    finally:
        if db is not None:
            db.close()
