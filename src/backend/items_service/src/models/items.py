from sqlalchemy import Column, ForeignKey, Integer, String

from src.db.database import BaseItems

class Items(BaseItems):
    __tablename__ = 'items'
    
    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    item_category_id = Column(Integer, ForeignKey('item_categories.item_category_id'), nullable=False)