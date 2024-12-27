import uuid
from abc import ABC, abstractmethod
from src.schemas.orders import *
from src.models.orders import Order
from src.schemas.result import Result, Error, GenResult
from src.storage.order import OrderRepository
from sqlalchemy.orm import joinedload
from typing import List


class OrderHandlerABC(ABC):
    @abstractmethod
    async def create_order(self, order: CreateOrderDto) -> GenResult[None]:
        pass

    @abstractmethod
    async def get_order(self, order_id: uuid) -> GenResult[OrderDto]:
        pass

    @abstractmethod
    async def get_user_orders(self, user_id: uuid) -> GenResult[List[OrderDto]]:
        pass

    @abstractmethod
    async def update_status(self, order_dto: UpdateOrderDto) -> GenResult[None]:
        pass


class OrderHandler(OrderHandlerABC):
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    async def create_order(self, order_dto: CreateOrderDto) -> GenResult[None]:
        await self._repository.insert(body=order_dto)
        await self._repository.commit()
        return GenResult.success(None)

    async def get_order(self, order_id: uuid) -> GenResult[OrderDto]:
        order = await self._repository.get_by_id(entity_id=order_id,
                                                 options=[joinedload(Order.order_items)])
        if not order:
            return GenResult.failure(
                error=Error(code="NOT_FOUND", reason="Order not found")
            )
        else:
            items = [
                ItemDto(**{
                        'item_id': item.item_id,
                        'quantity': item.quantity
                        })
                for item in order.order_items
            ]
            return GenResult.success(OrderDto(
                user_id=order.user_id,
                items=items,
                order_id=order.id,
                status=str(order.status.value),
                creation_time=order.creation_time))

    async def get_user_orders(self, user_id: uuid) -> GenResult[List[OrderDto]]:
        resp = await self._repository.get_by_user(user_id=user_id)
        return GenResult.success(resp)
        


    async def update_status(self, order_dto: UpdateOrderDto) -> GenResult[None]:
        order = await self._repository.get_by_id(entity_id=order_dto.order_id)
        if not order:
            return GenResult.failure(error=Error(code="NOT_FOUND", reason="Order not found"))
        else:
            order.update_status(
                new_status=order_dto.status
            )
            await self._repository.commit()
            return GenResult.success(None)
