from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel

from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException

from .async_crud_repository import AsyncCrudRepository

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=int | str)


class AsyncMemoryRepository(AsyncCrudRepository[T, ID], Generic[T, ID]):

    def __init__(self, key_name: str, model_class: Type[T]):
        super().__init__()
        self.key_name = key_name
        self.memory: list[dict] = []
        self.model_class = model_class
        # Deveria passar dinamco

    async def create(self, entity: T) -> T:
        entity_dict = entity.model_dump(by_alias=True)
        entity_dict["created_at"] = utcnow()

        self.memory.append(entity_dict)

        return entity

    async def find_by_id(self, entity_id: ID) -> Optional[T]:
        result = next((r for r in self.memory if r.get(self.key_name) == entity_id), None)
        if result is not None:
            result = self.model_class(**result)
        return result

    @staticmethod
    def _can_filter(data: T, filters: dict | None) -> bool:
        filters = filters or {}

        for key, value in filters.items():
            if value is not None and data.get(key) != value:
                return False
        return True

    async def find(self, filters: dict, limit: int = 10, offset: int = 0, sort: Optional[dict] = None) -> List[T]:
        # Aplica os filtros nos dados em memória
        results = [item for item in self.memory if self._can_filter(item, filters)]

        if sort:
            # Remove espaços extras nas chaves de ordenação
            cleaned_sort = {k.strip(): v for k, v in sort.items()}

            for key, order in reversed(list(cleaned_sort.items())):
                descending = order == -1
                # Garante que o campo existe antes de ordenar
                results = [r for r in results if r.get(key) is not None]
                results = sorted(results, key=lambda r: r.get(key), reverse=descending)

        # Aplica a paginação
        sliced = results[offset : offset + limit]

        # Converte os dicionários em instâncias da model_class
        return [self.model_class(**entry) for entry in sliced]

    async def update(self, entity_id: ID, entity: Any) -> T:
        # Converte a entidade para dicionário, mantendo os aliases
        entity_dict = entity.model_dump(by_alias=True, exclude={"identity"}) if hasattr(entity, 'model_dump') else dict(entity)
        entity_dict["updated_at"] = utcnow()

        for index, doc in enumerate(self.memory):
            # Usa a chave correta (_id) para encontrar o documento
            if str(doc.get("_id")) == str(entity_id):
                # Atualiza o documento existente com os novos valores
                self.memory[index].update(entity_dict)
                # Retorna o documento atualizado como uma instância do modelo
                return self.model_class(**self.memory[index])
        return None

    async def delete_by_id(self, entity_id: ID) -> bool:
        current_document = await self.find_by_id(entity_id)
        
        if not current_document:
            # return None
            raise NotFoundException(
                details=[
                    {
                        "message": "Document not found",
                        "location": "path",
                        "slug": "document_not_found",
                        "field": self.key_name,
                        "ctx": {"entity_id": entity_id},
                    }
                ]
            )

        self.memory = [doc for doc in self.memory if doc.get(self.key_name) != entity_id]
