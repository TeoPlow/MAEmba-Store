from fastapi import APIRouter, Request
from src.core.logging import log

router = APIRouter()

@router.post("/create")
async def create_order(request: Request):
    pass

@router.get("/{order_id}")
async def get_order_info(request: Request):
    pass

@router.post("/update-status")
async def update_status(request: Request):
    pass