from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from src.handlers.category import CategoryHandlerABC
from src.schemas.categories import *
from src.schemas.result import GenResult
from src.models.categories import Category

router = APIRouter()


@router.get(
    "",
    description="Получение всех категорий",
    response_model=list[CategoryDto],
    response_description="Список категорий и их идентификаторов",
    summary="Получение всех категорий",
)
async def all_categories(
    categories_service: CategoryHandlerABC = Depends(),
):
    result = await categories_service.get_all()
    return result.response


@router.get(
    "/{category_id}",
    description="Получение информации о товаре",
    response_model=CategoryDto,
    response_description="Информация о товаре (наименование, цена, количество, номер категории)",
    summary="Получение информации о товаре",
)
async def get_category_by_id(
    category_id: int,
    categories_service: CategoryHandlerABC = Depends(),
):
    result: GenResult[CategoryDto] = await categories_service.get_category(category_id=category_id)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=result.error.reason)
    return result.response


@router.post(
    "",
    description="Добавление новой категории",
    response_description="Статус выполнения операции",
    summary="Добавление новой категории",
)
async def create_category(
    body: CreateCategoryDto,
    categories_service: CategoryHandlerABC = Depends(),
):
    result = await categories_service.create_category(body)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result.error.reason)
    return { "status": "success" }
