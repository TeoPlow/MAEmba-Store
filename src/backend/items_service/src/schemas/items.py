from pydantic import BaseModel, Field
from typing import Optional, List


# Base item representation
class ItemBase(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    stock: int = Field(..., gt=0)
    item_category_id: int


# Response schema for GET /item/{item_id}/
class ItemDto(ItemBase):
    item_id: int


# Request schema for GET /item/search/
class ItemSearchRequest(BaseModel):
    query: Optional[str] = Field(None, description="Строка, содержащаяся в названии товара")
    price_min: Optional[float] = Field(None, gt=0, description="Поиск товаров выше указанной цены")
    price_max: Optional[float] = Field(None, gt=0, description="Поиск товаров ниже указанной цены")


# Item details for search results
class ItemSearchResult(BaseModel):
    item_id: int
    name: str
    price: float


# Response schema for GET /item/search/
class ItemSearchDto(BaseModel):
    items: List[ItemSearchResult]


# Request schema for PUT /item/update-item/
class UpdateItemDto(ItemBase):
    item_id: int


# Request schema for POST /item
class CreateItemDto(ItemBase):
    pass
