from abc import ABC, abstractmethod
from src.schemas import categories
from src.models.categories import Category
from src.schemas.result import Result, Error, GenResult
from src.storage.category import CategoryRepository
from typing import List


class CategoryHandlerABC(ABC):
    @abstractmethod
    async def create_category(self, category: categories.CreateCategoryDto) -> GenResult[None]:
        pass

    @abstractmethod
    async def get_category(self, category_id: int) -> GenResult[categories.CategoryBase]:
        pass

    @abstractmethod
    async def get_all(self) -> GenResult[List[categories.CategoryBase]]:
        pass


class CategoryHandler(CategoryHandlerABC):
    def __init__(self, repository: CategoryRepository):
        self._repository = repository

    async def get_category(self, category_id) -> GenResult[categories.CategoryBase]:
        category = await self._repository.get_by_id(entity_id=category_id)
        if not category:
            return GenResult.failure(
                error=Error(code="NOT_FOUND", reason="Category not found")
            )
        else:
            return GenResult.success(category)

    async def get_all(self) -> GenResult[List[categories.CategoryDto]]:
        resp = await self._repository.get_all()
        resp = [categories.CategoryDto(**category.to_dict()) for category in resp]
        return GenResult.success(resp)

    async def create_category(self, category_dto: categories.CreateCategoryDto) -> GenResult[None]:
        await self._repository.insert(body=category_dto)
        await self._repository.commit()
        return GenResult.success(None)
