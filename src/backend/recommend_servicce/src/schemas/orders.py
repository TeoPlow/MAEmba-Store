import uuid
from pydantic import BaseModel, Field, UUID4
from typing import Optional, List, Literal
from datetime import datetime


class ItemDto(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)


class OrderBase(BaseModel):
    user_id: UUID4
    items: List[ItemDto]


# create order
class CreateOrderDto(OrderBase):
    pass


# update order
class UpdateOrderDto(BaseModel):
    order_id: UUID4
    status: Literal["CREATED", "CANCELLED", "DELIVERED"]


# get order result
class OrderDto(OrderBase):
    order_id: UUID4
    status: Literal["CREATED", "CANCELLED", "DELIVERED"]
    creation_time: datetime
