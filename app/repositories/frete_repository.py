from uuid import UUID

from app.common.exceptions import NotFoundException

from ..models import Frete
from .base import AsyncMemoryRepository
from ..api.common.schemas import Paginator
from typing import List

class FreteRepository(AsyncMemoryRepository[Frete, UUID]):

    async def find_by_name(self, name: str) -> Frete:
        """
        Busca um alguma coisa pelo nome.
        """
        result = next((s for s in self.memory if s["name"] == name), None)
        if result:
            return result
        raise NotFoundException()

    async def find_all(self, paginator: Paginator, filters: dict) -> List[Frete]:
        """
        Busca todos os fretes com paginação e filtragem por seller_id.
        """
        return await super().find(filters=filters, limit=paginator.limit, offset=paginator.offset, sort=paginator.get_sort_order())

    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Frete:
        """
        Busca um frete pela junção de seller_id + sku
        """
        result = next((frete for frete in self.memory if frete["seller_id"] == seller_id and frete["sku"] == sku), None)
        return result

    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str):
        """
        Remove um frete da memória com base no seller_id e sku.
        """
        self.memory = [frete for frete in self.memory if not (frete["seller_id"] == seller_id and frete["sku"] == sku)]


__all__ = ["FreteRepository"]
