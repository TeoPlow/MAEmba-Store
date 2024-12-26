from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.routers.item import router

app = FastAPI(default_response_class=ORJSONResponse)

# Подключение роутеров
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
