from pydantic import BaseModel, Field
from typing import Optional, List


class CategoryBase(BaseModel):
    category_name: str


class CategoryDto(CategoryBase):
    item_category_id: int


class CreateCategoryDto(CategoryBase):
    pass
