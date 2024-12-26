from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import BaseItems

class Semicategory(BaseItems):
    __tablename__ = "semicategories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    
    # Связь с категорией
    category = relationship("Category", back_populates="semicategories")
    # Связь с товарами
    items = relationship("Item", back_populates="semicategory")
