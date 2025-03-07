import os

from cryptography.fernet import Fernet
from pydantic_settings import BaseSettings
from pathlib import Path


class _Settings(BaseSettings):
    APP_NAME: str = "Secrtes Keeper"
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    SECRET_KEY: str = Path("secret.key").read_text()


settings = _Settings()
