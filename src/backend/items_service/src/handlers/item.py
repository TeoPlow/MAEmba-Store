from abc import ABC, abstractmethod
from src.schemas import items
from src.models.items import Item
from src.schemas.result import Result, Error, GenResult
from src.storage.item import ItemRepository
from typing import List


class ItemHandlerABC(ABC):
    @abstractmethod
    async def create_item(self, item: items.CreateItemDto) -> GenResult[None]:
        pass
    
    
    @abstractmethod
    async def get_item(self, item_id: int) -> GenResult[items.ItemBase]:
        pass
    
    
    @abstractmethod
    async def search_items(self, request: items.ItemSearchRequest) -> GenResult[List[items.ItemBase]]:
        pass
    
    
    @abstractmethod
    async def update_item(self, item_dto: items.UpdateItemDto) -> GenResult[None]:
        pass
    
    
class ItemHandler(ItemHandlerABC):
    def __init__(self, repository: ItemRepository):
        self._repository = repository


    async def get_item(self, item_id) -> GenResult[items.ItemBase]:
        item = await self._repository.get_by_id(entity_id=item_id)
        if not item:
            return GenResult.failure(
                error=Error(code="NOT_FOUND", reason="Item not found")
            )
        else:
            return GenResult.success(item)


    async def search_items(self, request: items.ItemSearchRequest) -> GenResult[List[items.ItemBase]]:
        resp = await self._repository.search_item(query=request.query, min_price=request.price_min, max_price=request.price_max)
        return GenResult.success(resp)
    
    
    async def create_item(self, item_dto: items.CreateItemDto) -> GenResult[None]:
        await self._repository.insert(body=item_dto)
        await self._repository.commit()
        return GenResult.success(None)
        
        
    async def update_item(self, item_dto) -> GenResult[None]:
        item = await self._repository.get_by_id(entity_id=item_dto.item_id)
        if not item:
            return GenResult.failure(error=Error(code="NOT_FOUND", reason="Item not found"))
        else:
            item.update_item(
                name=item_dto.name,
                price=item_dto.price,
                stock=item_dto.stock,
                item_category_id=item_dto.item_category_id
            )
            await self._repository.commit()
            return GenResult.success(None)

        