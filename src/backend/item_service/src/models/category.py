from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.db.database import BaseItems

class Category(BaseItems):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Связь с подкатегориями
    semicategories = relationship("Semicategory", back_populates="category")
