from sqlalchemy import (
    UUID,
    Column,
    Integer,
    Float,
    DateTime,
)
from datetime import datetime, timezone
from src.db.database import BaseCart
from uuid import uuid4
from src.core.exceptions import SpecialException
from src.core.logging import log


class Cart(BaseCart):
    """
    Хранит информацию о товарах в корзине пользователя.
    """
    __tablename__ = "cart"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    def __init__(self, user_id: UUID, item_id: int, quantity: int, price: float):
        self.user_id = self.check_user_id(user_id)
        self.item_id = self.check_item_id(item_id)
        self.quantity = self.check_quantity(quantity)
        self.price = self.check_price(price)
        self.time = datetime.now(timezone.utc)

    def check_user_id(self, value: UUID) -> UUID:
        return value

    def check_item_id(self, value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise SpecialException("item_id должен быть положительным числом.")
        return value

    def check_quantity(self, value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise SpecialException("quantity должен быть положительным числом.")
        return value

    def check_price(self, value: float) -> float:
        if not isinstance(value, (int, float)) or value <= 0:
            raise SpecialException("price должен быть положительным числом.")
        return value

    def to_dict(self) -> dict:
        """
        Конвертирует объект Cart в словарь.
        """
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "item_id": self.item_id,
            "quantity": self.quantity,
            "price": self.price,
            "time": self.time.isoformat(),
        }

    @classmethod
    def validate_data(cls, data: dict) -> "Cart":
        """
        Проверяет данные для создания экземпляра Cart.
        """
        try:
            return cls(
                user_id=data["user_id"],
                item_id=data["item_id"],
                quantity=data["quantity"],
                price=data["price"],
            )
        except KeyError as e:
            raise SpecialException(f"Отсутствует обязательное поле: {e}")
        except ValueError as e:
            raise SpecialException(f"Ошибка валидации данных: {e}")
