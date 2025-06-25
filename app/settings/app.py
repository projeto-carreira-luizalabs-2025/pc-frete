from pydantic import Field, MongoDsn

from .base import BaseSettings


class AppSettings(BaseSettings):
    app_env: str = Field(..., description="Ambiente da aplicação")
    app_version: str = Field("0.2.1", description="Versão da aplicação")

    app_name: str = Field(
        default="PC frete",
        title="Módulo de frete",
        description="Microsserviço responsável por gerenciar os valores do frete",
    )

    memory_min: int = Field(default=64, title="Limite mínimo de memória disponível em MB")
    disk_usage_max: int = Field(default=80, title="Limite máximo de 80% de uso de disco")

    app_db_url: MongoDsn = Field(..., title="URI para o MongoDB")

settings = AppSettings()
