from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    ENVIRONMENT: str

    DATABASE_URL: str

    API_V1_PREFIX: str = "/api/v1"

    LOG_LEVEL: str = "INFO"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CIRCLE_API_KEY: str = ""
    CIRCLE_BASE_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()