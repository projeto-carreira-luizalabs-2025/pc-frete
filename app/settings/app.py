from pydantic import Field
from pydantic import Field, MongoDsn
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=False)
    version: str = Field("0.2.1", description="Versão da aplicação")
    app_db_url_mongo: MongoDsn = Field(..., title="URI para o MongoDB")
    MONGO_DB: str = Field(..., title="Nome do banco de dados padrão")
    app_name: str = Field(
        default="PC frete",
        title="Módulo de frete",
        description="Microsserviço responsável por gerenciar os valores do frete",
    )

    memory_min: int = Field(default=64, title="Limite mínimo de memória disponível em MB")
    disk_usage_max: int = Field(default=80, title="Limite máximo de 80% de uso de disco")


settings = AppSettings()
