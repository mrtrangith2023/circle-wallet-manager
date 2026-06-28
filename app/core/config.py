from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    CIRCLE_API_KEY: str
    CIRCLE_BASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()