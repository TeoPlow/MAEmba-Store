from abc import ABC, abstractmethod
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound
from src.db.postgres import Base
from typing import Generic, TypeVar, Type

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryABC(ABC):
    """
    Базовый абстрактный класс для репозиториев.
    Определяет основные операции с хранилищем.
    """

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        """
        Получить сущность по ID.
        """
        pass

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        """
        Получить список всех сущностей.
        """
        pass

    @abstractmethod
    async def insert(self, *args, **kwargs):
        """
        Создать новую сущность.
        """
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        """
        Удалить сущность по ID.
        """
        pass
    
    
    async def commit(self, *args, **kwargs) -> None:
        pass


class PostgresRepository(RepositoryABC, Generic[ModelType, CreateSchemaType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self._model = model
        self._session = session
    
    
    async def get_all(self) -> list[ModelType]:
        statement = select(self._model)
        results = await self._session.execute(statement)
        return results.scalars().all()
    
    
    async def get_by_id(self, *, entity_id: int) -> ModelType:
        statement = select(self._model).where(self._model.id == entity_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()


    async def insert(self, body: CreateSchemaType) -> ModelType:
        raw_obj = jsonable_encoder(body)
        database_obj = self._model(**raw_obj)
        self._session.add(database_obj)
        return database_obj
    

    async def delete(self, *, entity_id: int) -> None:
        await self._session.delete(self._model).where(self._model.id == entity_id)


    async def commit(self, *args, **kwargs) -> None:
        return await self._session.commit()