from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_url: str = Field(default='postgres')
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(...)
    postgres_password: str = Field(...)
    postgres_db: str = Field(...)


settings = Settings()
