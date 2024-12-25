from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from src.handlers.item import ItemHandlerABC
from src.schemas.items import *
from src.schemas.result import GenResult
from src.models.items import Item

router = APIRouter()


@router.get("/ping")
def ping_pong():
    return "pong"


@router.get(
    "/item/search",
    description="Поиск товаров по имени и цене",
    response_model=list[ItemBase],
    response_description="Список товаров, удовлетворяющих параметрам поиска",
    summary="Поиск товаров по имени и цене",
)
async def search_items(
    body: ItemSearchRequest,
    items_service: ItemHandlerABC = Depends(),
):
    result = await items_service.search_items(body)
    return result.response


@router.get(
    "/item/{item_id}",
    description="Получение информации о товаре",
    response_model=ItemBase,
    response_description="Информация о товаре (наименование, цена, количество, номер категории)",
    summary="Получение информации о товаре",
)
async def get_item_by_id(
    item_id: int,
    items_service: ItemHandlerABC = Depends(),
):
    result: GenResult[ItemBase] = await items_service.get_item(item_id=item_id)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=result.error.reason)
    return result.response


@router.put(
    "/item",
    description="Обновление данных о товаре",
    response_description="Статус выполнения операции",
    summary="Обновление данных о товаре",
)
async def update_item(
    body: UpdateItemDto,
    items_service: ItemHandlerABC = Depends(),
):
    result = await items_service.update_item(body)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result.error.reason)
    return { "status": "success" }


@router.post(
    "/item",
    description="Добавление нового товара",
    response_description="Статус выполнения операции",
    summary="Добавление нового товара",
)
async def create_item(
    body: CreateItemDto,
    items_service: ItemHandlerABC = Depends(),
):
    result = await items_service.create_item(body)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result.error.reason)
    return { "status": "success" }
