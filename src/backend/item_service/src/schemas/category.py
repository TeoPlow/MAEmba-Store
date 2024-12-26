from pydantic import BaseModel
from typing import List, Optional
from src.schemas.semicategory import SemicategorySchema

class CategorySchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    semicategories: List[SemicategorySchema] = []
    
    class Config:
        orm_mode = True