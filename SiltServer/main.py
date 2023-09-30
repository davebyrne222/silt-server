import uvicorn
from fastapi import FastAPI
import logging
import logging.config
from pydantic_settings import BaseSettings

from SiltServer.database.database import engine, Base
from SiltServer.routers import songs as songs_router, auth as auth_router

logging.config.fileConfig('logging_config.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Loads from .env"""
    SERVER_ADDR_HOST: str = "0.0.0.0"
    SERVER_ADDR_PORT: int = 8081
    SERVER_RELOAD: bool = False


settings = Settings()

logger.debug(f"Settings: {vars(settings)}")

# Create tables from SQLAlchemy models
Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(songs_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.SERVER_ADDR_HOST,
                port=settings.SERVER_ADDR_PORT,
                reload=settings.SERVER_RELOAD,
                log_config="logging_config.ini",
                )

