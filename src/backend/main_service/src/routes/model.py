from fastapi import APIRouter, Request
import logging
import logging.config
from core.logging import log

router = APIRouter()

@router.get("/recommendation")
async def recomendation(request: Request):
    pass

@router.get("/predict")
async def predict(request: Request):
    pass