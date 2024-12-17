from fastapi import FastAPI

from src.core.exceptions import SpecialException
from src.routes import cart
from src.core.exceptions import special_exception_handler


app = FastAPI()

app.include_router(cart.router, prefix="", tags=["Get, Put, Delete items in cart."])

@app.get("/")
async def root():
    return {"message": "Это Cart API для проекта MAEMBA Store"}

app.add_exception_handler(SpecialException, special_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)