from fastapi import FastAPI
from routes import user, model, items, cart, order

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["User Management and Auth"])
app.include_router(model.router, prefix="/model", tags=["Recomendation and Predict model"])
app.include_router(items.router, prefix="/item", tags=["Items"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(order.router, prefix="/order", tags=["Order"])

@app.get("/")
async def root():
    return {"message": "Это Main API для проекта MAEMBA Store"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


