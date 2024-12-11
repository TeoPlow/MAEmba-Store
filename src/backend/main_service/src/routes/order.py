from fastapi import APIRouter, Request
import logging
import logging.config
from core.config import logger_config, log

logging.config.dictConfig(logger_config)

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