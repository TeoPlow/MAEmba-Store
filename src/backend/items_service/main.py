from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.routes import items, categories
from src.core.exceptions import SpecialException
from src.core.exceptions import special_exception_handler

app = FastAPI(
    default_response_class=ORJSONResponse,
)

app.include_router(items.router, prefix="/item")
app.include_router(categories.router, prefix="/category")

app.add_exception_handler(SpecialException, special_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)