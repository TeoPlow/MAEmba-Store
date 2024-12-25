import uuid
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, String
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, Float, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as PyEnum
from datetime import datetime, timezone

Base = declarative_base()


class Status(str, PyEnum):
    CREATED = "CREATED"
    CANCELLED = "CANCELLED"
    DELIVERED = "DELIVERED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    status = Column(Enum(Status), default=Status.CREATED, nullable=False)
    creation_time = Column(DateTime(timezone=True),
                           default=datetime.now(timezone.utc))

    # Связь с таблицей OrderItems
    order_items = relationship(
        'OrderItem', back_populates='order', cascade='all, delete-orphan')

    def update_status(self, new_status):
        """Метод для обновления статуса заказа."""
        if new_status not in Status:
            raise ValueError(f"Invalid status: {new_status}")

        self.status = new_status

    def to_dict(self) -> dict:
        return {
            "order_id": self.id,
            "status": self.status.value,
            "user_id": self.user_id,
            "items": [
                {
                    "item_id": item.item_id,
                    "quantity": item.quantity,
                }
                for item in self.order_items
            ],
            "creation_time": self.creation_time,
        }


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(UUID, ForeignKey('orders.id'),
                      nullable=False)  # Внешний ключ на заказ
    item_id = Column(Integer)  # ID продукта
    quantity = Column(Integer)  # Количество продукта

    # Связь с таблицей Order
    order = relationship('Order', back_populates='order_items')
