from dependency_injector import containers, providers

from app.models import Frete
from app.repositories import FreteRepository
from app.services import FreteService, HealthCheckService
from app.settings import AppSettings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # Repositórios
    frete_repository = providers.Singleton(FreteRepository, key_name="id", model_class=Frete)

    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    frete_service = providers.Singleton(FreteService, repository=frete_repository)
