from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, Float, Text
from src.db.postgres import Base


class Category(Base):
    __tablename__ = "categories"

    item_category_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "item_category_id": self.item_category_id,
            "category_name": self.category_name
        }

    def update_item(self, name, price, stock, item_category_id):
        self.name = name
        self.price = price
        self.stock = stock
        self.item_category_id = item_category_id
