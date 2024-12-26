from uuid import UUID
from pydantic import BaseModel
from typing import List
from datetime import datetime


# Схема для GET /{user_id} (Получить корзину пользователя)
class CartItem(BaseModel):
    id: UUID
    user_id: UUID
    item_id: int
    quantity: int
    price: float
    time: datetime


class GetCartResponse(BaseModel):
    status: str
    data: dict[str, List[CartItem]]


# Схема для PUT /{user_id} (Обновить корзину пользователя)
class UpdateCartRequest(BaseModel):
    item_id: int
    quantity: int
    price: float


class UpdateCartResponse(BaseModel):
    status: str


# Схема для DELETE /{user_id} (Удалить товар из корзины)
class DeleteCartItemRequest(BaseModel):
    item_id: int


class DeleteCartItemResponse(BaseModel):
    status: str
