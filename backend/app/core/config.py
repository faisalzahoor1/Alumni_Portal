# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    API_PREFIX: str

    MONGODB_URL: str
    DATABASE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()