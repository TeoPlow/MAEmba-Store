from fastapi import APIRouter, Request
import logging
import logging.config
from core.config import logger_config, log

logging.config.dictConfig(logger_config)

router = APIRouter()

@router.get("/recommendation")
async def recomendation(request: Request):
    pass

@router.get("/predict")
async def predict(request: Request):
    pass