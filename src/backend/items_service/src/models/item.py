from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from db.database import BaseItems

class Item(BaseItems):
    __tablename__ = "item"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255))
    card_url = Column(String(255))
    rating = Column(Float, default=0, nullable=False)
    price = Column(Float, nullable=False)
    item_category_id = Column(Integer, ForeignKey("item_categories.item_category_id"), nullable=True)

    # Связь с категорией
    category = relationship("ItemCategory", back_populates="items")