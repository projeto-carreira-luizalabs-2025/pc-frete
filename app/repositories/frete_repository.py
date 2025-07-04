from typing import Optional
from uuid import UUID

from app.common.exceptions import NotFoundException

from ..models import Frete
from .base import AsyncMemoryRepository
from ..api.common.schemas import Paginator
from typing import List

from app.integrations.database.mongo_client import MongoClient

class FreteRepository(AsyncMemoryRepository[Frete]):

    COLLECTION_NAME = "fretes"

    def __init__(self,client: "MongoClient", db_name: str):
        super().__init__(client, db_name=db_name, collection_name=self.COLLECTION_NAME, model_class=Frete)

    async def find_by_name(self, name: str) -> Optional[Frete]:
        """
        Busca um alguma coisa pelo nome.
        """
        return await self.find_by_id({"sku": name})

    async def find_all(self, paginator: Paginator, filters: dict) -> List[Frete]:
        """
        Busca todos os fretes com paginação e filtragem por seller_id.
        """
        # return await self.find(
        #     filters=filters,
        #     limit=paginator.limit,
        #     offset=paginator.offset,
        #     sort=paginator.get_sort_order()
        # )
        return []
        # return await super().find(filters=filters, limit=paginator.limit, offset=paginator.offset, sort=paginator.get_sort_order())

    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Frete | None:
        """
        Busca um frete pela junção de seller_id + sku
        """

        return await self.find_by_id({"seller_id": seller_id, "sku": sku})

    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str):
        """
        Remove um frete da memória com base no seller_id e sku.
        """

        frete = await self.find_by_seller_id_and_sku(seller_id, sku)
        if not frete:
            raise NotFoundException()
        await self.delete_by_id(

__all__ = ["FreteRepository"]
