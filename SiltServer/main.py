import os

import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from pydantic_settings import BaseSettings

from auth import router as auth_router
from songs import router as songs_router


class Settings(BaseSettings):
    """Loads from .env"""
    SERVER_ADDR_HOST: str = "0.0.0.0"
    SERVER_ADDR_PORT: int = 8081
    SERVER_RELOAD: bool = False


settings = Settings()

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

app.include_router(auth_router.router)
app.include_router(songs_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.SERVER_ADDR_HOST,
                port=settings.SERVER_ADDR_PORT,
                reload=settings.SERVER_RELOAD
                )
