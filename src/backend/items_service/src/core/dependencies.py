from typing import Callable, Type
from functools import cache
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, FastAPI
from src.handlers.item import *
from src.db.postgres import get_session
import logging

dependencies_container: dict[Type | Callable, Callable] = {}


def add_factory_to_mapper(cls: Type | Callable):
    """
    Декоратор для добавления функции в dependencies_container
    """
    def _add_factory_to_mapper(func: Callable):
        dependencies_container[cls] = func
        return func
    
    return _add_factory_to_mapper


@add_factory_to_mapper(ItemHandlerABC)
@cache
def create_item_service(session: AsyncSession = Depends(get_session)) -> ItemHandlerABC:
    repository = ItemRepository(session=session)
    return ItemHandler(repository)


def setup_dependencies(app: FastAPI, mapper: dict[Type | Callable, Callable] | None = None) -> None:
    if mapper is None:
        mapper = dependencies_container
    for interface, dependency in mapper.items():
        app.dependency_overrides[interface] = dependency
    logging.info("Dependencies mapping: %s", app.dependency_overrides)
