from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    # postgres_url: str = Field(default='postgres')
    # postgres_port: int = Field(default=5432)
    # postgres_user: str = Field(...)
    # postgres_password: str = Field(...)
    # postgres_db: str = Field(...)
    gigachat_credentials: str | None = Field(description='токен для доступа к gigachat', default=None)
    gigachat_model: str = Field(
        description='фикс используемой gigachat модели',
        default='GigaChat',  # тэги вида `:latest` кажется отбрасываются (в списке моделей их нет)
    )
    saiga_model_name: str = Field(
        description='версия модельки saiga',
        default='IlyaGusev/saiga_llama3_8b',
    )
    huggingface_token: str | None = Field(description='токен для доступа к huggingface', default=None)


settings = _Settings()
