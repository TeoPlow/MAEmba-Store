import requests
from uuid import UUID
from typing import Any

from src.models.Cart import Cart
from src.db.database import get_db_cart
from src.core.config import ITEM_API_URL
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
        log.debug(f"Добавляю/обновляю товар {item_id} с количеством {quantity} для пользователя {user_id}")
        
        url = ITEM_API_URL + f"/{item_id}"
        headers = {"Content-Type": "application/json"}

        # response = requests.get(url, headers=headers)
        # response.raise_for_status()
        # result = response.json()
        result = {"price": 119.90} # временно без ITEM API, пока мастер Евген страдает ******
        log.debug(f"Получил от ITEM API: {result}")

        cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.item_id == item_id).first()
        
        sum_price = round(result["price"] * quantity, 2)

        if cart_item:
            log.debug(f"Товар {item_id} уже есть в корзине. Обновляю количество и цену.")
            cart_item.quantity = quantity
            cart_item.price = sum_price
        else:
            log.debug(f"Товар {item_id} отсутствует в корзине. Добавляю новый товар.")
            new_cart_item = Cart(user_id, item_id, quantity, price=sum_price)
            db.add(new_cart_item)
        
        db.commit()
        log.debug(f"Товар {item_id} успешно добавлен/обновлён для пользователя {user_id}.")
    finally:
        if db is not None:
            db.close()
