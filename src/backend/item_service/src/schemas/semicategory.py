from pydantic import BaseModel
from typing import List, Optional
from src.schemas.item import ItemSchema

class SemicategorySchema(BaseModel):
    id: int
    name: str
    category_id: int
    items: List[ItemSchema] = []
    
    class Config:
        orm_mode = True