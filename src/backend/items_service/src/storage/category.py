from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.storage.base import RepositoryABC, PostgresRepository
from src.schemas.categories import CreateCategoryDto
from src.models.categories import Category


class CategoryRepositoryABC(RepositoryABC, ABC):
    pass


class CategoryRepository(PostgresRepository[Category, CreateCategoryDto], CategoryRepositoryABC):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Category)
