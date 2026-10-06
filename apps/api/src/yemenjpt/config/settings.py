"""Application settings — all config from environment variables."""
from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "YemenJPT API"
    APP_VERSION: str = "0.1.0"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://yemenjpt:yemenjpt_dev@localhost:5432/yemenjpt"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Security
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-64-hex"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    # AI / Model routing
    MODEL_PROVIDER: str = "mock"   # "mock" | "openai" | "ollama"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    MODEL_REASONING: str = "gpt-4o"
    MODEL_EXTRACTION: str = "gpt-4o-mini"
    MODEL_CLASSIFICATION: str = "gpt-4o-mini"
    MODEL_EMBEDDING: str = "text-embedding-3-small"
    MODEL_TRANSLATION: str = "gpt-4o-mini"
    MODEL_VISION: str = "gpt-4o"

    # Archive / storage
    ARCHIVE_BASE_PATH: str = "./data/archive"

    # Event Bus
    EVENT_BUS_MAX_RETRIES: int = 3

@lru_cache
def get_settings() -> Settings:
    return Settings()
