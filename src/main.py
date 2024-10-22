from fastapi import FastAPI

from src.users.routers import router

app = FastAPI(description="Users API")
app.include_router(router, prefix="/api/v1")
