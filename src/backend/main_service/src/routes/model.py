from fastapi import APIRouter, Request
from src.core.logging import log

router = APIRouter()

@router.get("/recommendation")
async def recomendation(request: Request):
    pass

@router.get("/predict")
async def predict(request: Request):
    pass