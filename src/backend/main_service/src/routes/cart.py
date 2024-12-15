from fastapi import APIRouter, Request
from src.core.logging import log

router = APIRouter()

@router.get("/{user_id}")
async def get_cart_info(request: Request):
    pass

@router.post("/add-item")
async def add_item(request: Request):
    pass

@router.post("/remove-item")
async def remove_item(request: Request):
    pass