# container.py
from app.integrations.database.mongo_client import MongoClient
from dependency_injector import containers, providers

from app.repositories import FreteRepository
from app.services import FreteService, HealthCheckService
from app.settings.app import AppSettings
from app.settings.app import settings as settings_instance

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(settings_instance)
    settings = providers.Singleton(AppSettings.model_validate, config)

    mongo_client = providers.Singleton(
        MongoClient,
        mongo_url=config.app_db_url_mongo,
    )

    frete_repository = providers.Singleton(
        FreteRepository,
        client=mongo_client,
        db_name=config.MONGO_DB,
    )

    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    frete_service = providers.Singleton(FreteService, repository=frete_repository)
