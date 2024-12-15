from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.storage.base import RepositoryABC, PostgresRepository
from src.schemas.items import CreateItemDto
from src.models.items import Item

class ItemRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def search_item(self, *, query: str, min_price: float, max_price: float):
        """
        Выполняет поиск товаров, имя которых содержит `query`, и цена которых
        находится в диапазоне от `min_price` до `max_price`.
        """
        pass
    

class ItemRepository(PostgresRepository[Item, CreateItemDto], ItemRepositoryABC):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Item)
    
    
    async def search_item(self, *, query: str, min_price: float, max_price: float):
        if not min_price:
            min_price = 0
        if not max_price:
            max_price = float('inf')
        if not query:
            query = ""
            
        statement = (
            select(self._model)
            .where(
                self._model.name.ilike(f"%{query}%"),
                self._model.price >= min_price,
                self._model.price <= max_price,
            )
        )
        results = await self._session.execute(statement)
        return results.scalars().all()
