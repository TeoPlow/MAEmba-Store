from fastapi import FastAPI

from src.core.exceptions import SpecialException
from src.routes import auth, connect
from src.core.exceptions import special_exception_handler


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentification and Registration"])
app.include_router(connect.router, prefix="", tags=["Get and Put User ID"])

@app.get("/")
async def root():
    return {"message": "Это User API для проекта MAEMBA Store"}

app.add_exception_handler(SpecialException, special_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)