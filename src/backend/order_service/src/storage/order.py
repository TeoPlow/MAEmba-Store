import uuid
from abc import ABC, abstractmethod
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.storage.base import RepositoryABC, PostgresRepository
from src.schemas.orders import CreateOrderDto, OrderDto
from src.models.orders import Order, OrderItem
from sqlalchemy.orm import joinedload
from typing import List


class OrderRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def get_by_user(self, *, user_id: uuid):
        """
        Получает все заказы пользователя с таким user_id.
        """
        pass


class OrderRepository(PostgresRepository[Order, CreateOrderDto], OrderRepositoryABC):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Order)

    async def insert(self, body: CreateOrderDto) -> Order:
        raw_order = jsonable_encoder(
            body, exclude={"items"})  # Исключаем `items`
        order = Order(**raw_order)
        self._session.add(order)
        await self._session.flush()  # Генерация `order_id` после вставки

        # Добавляем связанные товары
        items = [
            OrderItem(order_id=order.id,
                      item_id=item.item_id, quantity=item.quantity)
            for item in body.items
        ]
        self._session.add_all(items)

        # Сохраняем изменения в базе
        await self._session.commit()
        await self._session.refresh(order)
        return order

    async def get_by_user(self, *, user_id: uuid.UUID) -> List[OrderDto]:
        # Загрузка заказов с привязанными элементами
        statement = (
            select(self._model)
            .where(self._model.user_id == user_id)
            .options(joinedload(self._model.order_items))  # Предзагрузка связи
        )
        results = await self._session.execute(statement)
        orders = results.unique().scalars().all()

        # Преобразование в массив словарей
        orders_with_items = [
            order.to_dict()
            for order in orders
        ]
        return orders_with_items
