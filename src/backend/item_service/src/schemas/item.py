from pydantic import BaseModel
from typing import Optional

class ItemSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    rating: float
    price: float
    semicategory_id: int
    card_url: Optional[str]
    
    class Config:
        orm_mode = True