from typing import Any, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from bson import ObjectId

from app.common.datetime import utcnow
from app.integrations.database.mongo_client import MongoClient
from app.models.query_model import QueryModel

from .async_crud_repository import AsyncCrudRepository

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=UUID)
Q = TypeVar("Q", bound=QueryModel)


DEFAULT_USER = "system"

class AsyncMemoryRepository(AsyncCrudRepository[T], Generic[T]):

    def __init__(self, client: MongoClient, db_name: str, collection_name: str, model_class: Type[T]):
        """
        Repositório genérico para MongoDB.

        :param client: Instância do MongoClient.
        :param db_name: Nome do banco de dados a ser utilizado.
        :param collection_name: Nome da coleção.
        :param model_class: Classe do modelo (usada para criar instâncias de saída).
        """
        database = client.get_database(db_name)
        self.collection = database[collection_name]
        self.model_class = model_class

    async def create(self, entity: T) -> T:
        now = utcnow()
        entity_dict = entity.model_dump(by_alias=True)
        entity_dict.setdefault("created_at", now)
        entity_dict.setdefault("updated_at", now)
        entity_dict.setdefault("created_by", DEFAULT_USER)
        entity_dict.setdefault("updated_by", DEFAULT_USER)
        entity_dict.setdefault("audit_created_at", now)
        entity_dict.setdefault("audit_updated_at", now)
        await self.collection.insert_one(entity_dict)
        return self.model_class(**entity_dict)

    async def find_by_id(self, entity_id: Any) -> Optional[T]:
        # converter entity_id para ObjectId se possível
        try:
            oid = ObjectId(entity_id)
        except Exception:
            # se não for um ObjectId válido, usa como string mesmo
            oid = entity_id

        result = await self.collection.find_one({"_id": oid})
        if result:
            return self.model_class(**result)
        return None

    async def find(self, filters: dict, limit: int = 10, offset: int = 0, sort: Optional[dict] = None) -> List[T]:
        cursor = self.collection.find(filters)
        if sort:
            # sort: {"field": 1/-1}
            cursor = cursor.sort(list(sort.items()))
        cursor = cursor.skip(offset).limit(limit)
        results = []
        async for doc in cursor:
            results.append(self.model_class(**doc))
        return results

    async def update(self, seller_id: str, entity: Any) -> Optional[T]:
        # PUT: substitui todos os campos (menos _id)
        entity_dict = entity.model_dump(by_alias=True, exclude={"identity"})
        result = await self.collection.find_one_and_update(
            {"seller_id": str(seller_id)}, {"$set": entity_dict}, return_document=True
        )
        if result:
            return self.model_class(**result)
        return None

    async def delete_by_id(self, seller_id: str) -> bool:
        result = await self.collection.delete_one({"seller_id": str(seller_id)})
        return result.deleted_count > 0

    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str) -> bool:
        result = await self.collection.delete_one({"seller_id": str(seller_id), "sku": sku})
        return result.deleted_count > 0

    async def patch(self, seller_id: str, update_fields: dict) -> Optional[T]:
        # PATCH: atualiza só os campos enviados
        result = await self.collection.find_one_and_update(
            {"seller_id": str(seller_id)}, {"$set": update_fields}, return_document=True
        )
        if result:
            return self.model_class(**result)
        return None
