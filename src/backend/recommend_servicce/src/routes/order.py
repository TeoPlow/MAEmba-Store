from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from src.handlers.order import OrderHandlerABC
from src.schemas.orders import *
from src.schemas.result import GenResult
from src.models.orders import Order

router = APIRouter()

@router.get("/ping")
def ping_pong():
    return "pong"


@router.get(
    "/user={user_id}",
    description="Получение всех заказов пользователя",
    response_model=List[OrderDto],
    response_description="Список заказов пользователя",
    summary="Получение всех заказов пользователя",
)
async def user_orders(
    user_id: uuid.UUID,
    order_service: OrderHandlerABC = Depends(),
):
    result = await order_service.get_user_orders(user_id)
    return result.response


@router.get(
    "/order={order_id}",
    description="Получение информации о заказе",
    response_model=OrderDto,
    response_description="""Информация о заказе
    (идентификатор заказа, пользователя,
    товары в заказе и их количество,
    статус заказа, время создания заказа)""",
    summary="Получение информации о заказе",
)
async def get_order_by_id(
    order_id: uuid.UUID,
    order_service: OrderHandlerABC = Depends(),
):
    result: GenResult[OrderDto] = await order_service.get_order(order_id)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=result.error.reason)
    return result.response


@router.put(
    "/update-status",
    description="Обновление данных о статусе заказа",
    response_description="Статус выполнения операции",
    summary="Обновление данных о статусе заказа",
)
async def update_status(
    body: UpdateOrderDto,
    order_service: OrderHandlerABC = Depends(),
):
    result = await order_service.update_status(body)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=result.error.reason)
    return {"status": "success"}


@router.post(
    "/",
    description="Добавление нового заказа",
    response_description="Статус выполнения операции",
    summary="Добавление нового заказа",
)
async def create_order(
    body: CreateOrderDto,
    order_service: OrderHandlerABC = Depends(),
):
    result = await order_service.create_order(body)
    if not result.is_success:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=result.error.reason)
    return {"status": "success"}
