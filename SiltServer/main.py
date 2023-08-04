import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings

from SiltServer.routers import auth as auth_router, songs as songs_router


class Settings(BaseSettings):
    """Loads from .env"""
    SERVER_ADDR_HOST: str = "0.0.0.0"
    SERVER_ADDR_PORT: int = 8081
    SERVER_RELOAD: bool = False


settings = Settings()

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(songs_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.SERVER_ADDR_HOST,
                port=settings.SERVER_ADDR_PORT,
                reload=settings.SERVER_RELOAD
                )
