from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from src.db.database import BaseItems

class ItemCategory(BaseItems):
    __tablename__ = 'item_categories'
    
    item_category_name = Column(String, nullable=False)
    item_category_id = Column(String, primary_key=True, index=True)
    
    # Связь с вложенными категориями и товарами
    subcategories = relationship("ItemCategory", backref="parent", remote_side=[item_category_id])
    items = relationship("Item", back_populates="category")