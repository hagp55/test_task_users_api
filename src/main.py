from fastapi import FastAPI

from src.users.routers import router

app = FastAPI()
app.include_router(router, prefix="/api")
