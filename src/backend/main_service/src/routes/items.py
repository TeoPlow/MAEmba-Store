from fastapi import APIRouter, Request
import logging
import logging.config
from core.config import logger_config, log

logging.config.dictConfig(logger_config)

router = APIRouter()

@router.get("/{item_id}")
async def get_item_info(request: Request):
    pass

@router.get("/search")
async def search(request: Request):
    pass

@router.post("/update-stock")
async def update_stock(request: Request):
    pass
