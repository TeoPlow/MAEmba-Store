from fastapi import FastAPI
from src.routers.item import router

app = FastAPI()

app.include_router(router, prefix="/api", tags=["Items"])