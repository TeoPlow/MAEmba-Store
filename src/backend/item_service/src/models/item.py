from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.db.database import BaseItems

class Item(BaseItems):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    rating = Column(Float, nullable=True, server_default="0")  # Значение по умолчанию для rating
    price = Column(Float, nullable=True, server_default="0")
    card_url = Column(String, nullable=True)
    semicategory_id = Column(Integer, ForeignKey("semicategories.id"), nullable=False)
    
    # Связь с подкатегорией
    semicategory = relationship("Semicategory", back_populates="items")
    # Даты
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())