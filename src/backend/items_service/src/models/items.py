from sqlalchemy import Column, Integer, String, Float, Text

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    item_category_id = Column(Integer, nullable=True)


    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name}, price={self.price}, quantity={self.stock})>"


    def update_item(self, name, price, stock, item_category_id):
        self.name = name
        self.price = price
        self.stock = stock
        self.item_category_id = item_category_id