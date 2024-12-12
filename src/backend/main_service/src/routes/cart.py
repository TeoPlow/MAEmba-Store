from fastapi import APIRouter, Request
import logging
import logging.config
from core.logging import logger_config, log

logging.config.dictConfig(logger_config)

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