from fastapi import FastAPI
from routes import auth, connect

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentification and Registration"])
app.include_router(connect.router, prefix="", tags=["Get and Put User ID"])

@app.get("/")
async def root():
    return {"message": "Это User API для проекта MAEMBA Store"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)