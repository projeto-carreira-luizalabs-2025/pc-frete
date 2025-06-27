from dependency_injector import containers, providers

from app.models import Frete
from app.repositories import FreteRepository
from app.services import FreteService, HealthCheckService
from app.settings import AppSettings
from app.integrations.database.mongo_client import MongoClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    mongo_client = providers.Singleton(MongoClient, config.app_db_url)

    # Repositórios
    frete_repository = providers.Singleton(
        FreteRepository, 
        client=mongo_client,
    )

    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    frete_service = providers.Singleton(FreteService, repository=frete_repository)
