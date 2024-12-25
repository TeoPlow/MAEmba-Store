from sqlalchemy import Column, ForeignKey, Integer, String

from src.db.database import BaseItems

class Items(BaseItems):
    __tablename__ = 'items'
    
    item_name = Column(String, nullable=False)
    item_id = Column(String, primary_key=True, index=True)
    item_category_id = Column(String, ForeignKey('item_categories.item_category_id'), nullable=False)