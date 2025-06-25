from uuid import UUID

from app.common.exceptions import NotFoundException

from ..models import Frete
from .base.mongo_mktplace_repository import MongoMktplaceRepository
from app.integrations.database.mongo_client import MongoClient
from ..api.common.schemas import Paginator
from typing import List

class FreteRepository(MongoMktplaceRepository[Frete]):

    COLLECTION_NAME = "fretes"

    def __init__(self, client: MongoClient):
        super().__init__(
            client=client,
            collection_name=self.COLLECTION_NAME,
            model_class=Frete
        )

__all__ = ["FreteRepository"]
