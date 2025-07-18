from uuid import UUID

from ...api.common.schemas.response import ErrorDetail
from ...common.exceptions import BadRequestException
from ...models import Frete
from ...repositories import FreteRepository
from ..base import CrudService
from ...api.common.schemas import Paginator
from .frete_exceptions import FreteAlreadyExistsException, FreteNotFoundException

class FreteService(CrudService[Frete, UUID]):
    """
    Serviço responsável pelas regras de negócio relacionadas à entidade Frete.
    Fornece métodos para criação, atualização, busca e validação de fretes.
    """

    repository: FreteRepository

    def __init__(self, repository: FreteRepository):
        """
        Inicializa o serviço de fretes com o repositório fornecido.

        :param repository: Instância de FreteRepository para acesso aos dados.
        """
        super().__init__(repository)

    async def find_all(self, paginator: Paginator, filters: dict) -> list[Frete]:
        """
        Busca todos os fretes com paginação e filtros.
        """
        query_filters = {}

        if filters.get("seller_id"):
            query_filters["seller_id"] = filters["seller_id"]
        if filters.get("preco_greater_than") is not None:
            query_filters["valor"] = {"$gte": filters["preco_greater_than"]}
        if filters.get("preco_less_than") is not None:
            query_filters.setdefault("valor", {})
            query_filters["valor"]["$lte"] = filters["preco_less_than"]

        fretes = await self.repository.find_all(
            paginator=paginator,
            filters=query_filters
        )
        
        return fretes

    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Frete:
        """
        Busca um fretes pelo seller_id e sku.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :return: Instância de Frete encontrada.
        :raises FreteNotFoundException: Se não encontrar o frete.
        """

        fretes = await self._validate_frete_nao_existe(seller_id, sku)

        if not fretes:
            raise FreteNotFoundException(seller_id=seller_id, sku=sku)

        return fretes[0]  # ou como preferir lidar com múltiplos resultados

    async def create_frete(self, frete_create) -> Frete:
        """
        Cria uma novo frete após validações de unicidade e valores positivos.

        :param frete_create: Objeto contendo os dados para criação do fretes.
        :return: Instância de Frete criada.
        :raises BadRequestException: Se já existir fretes para o produto ou valores inválidos.
        """
        # Valida se já existe frete para o seller_id e sku informados
        await self._validate_frete_existe(frete_create.seller_id, frete_create.sku)
        self._validate_fretes_positivos(frete_create)
        
        # Converte FreteCreate para Frete, gerando o id automaticamente
        frete = Frete(**frete_create.model_dump())
        return await self.create(frete)

    async def update_frete_value(self, seller_id: str, sku: str, frete_update) -> Frete:
        frete_existente = await self._validate_frete_nao_existe(seller_id, sku)
        self._validate_fretes_positivos(frete_update)

        frete = frete_existente[0]
        id = frete.id

        # Pega apenas os campos que vieram no PATCH
        updates = frete_update.model_dump(exclude_unset=True)

        # Cria uma nova instância com os dados atualizados
        frete_atualizado = frete.model_copy(update=updates)

        # Atualiza no banco (essa função precisa salvar e retornar o Frete atualizado)
        updated = await self.update(id, frete_atualizado)

        # Retorna a versão final
        return updated

    async def replace_frete(self, seller_id: str, sku: str, frete_update) -> Frete:
        """
        Substitui completamente os dados de um frete existente.
        """
        frete_existente = await self._validate_frete_nao_existe(seller_id, sku)
        self._validate_fretes_positivos(frete_update)

        frete = frete_existente[0]

        novo_frete = Frete(**frete_update.model_dump())

        return await self.update(frete.id, novo_frete)

    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str):
        """
        Remove um frete baseado em seller_id e sku.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises NotFoundException: Se o frete não for encontrado.
        """
        frete_encontrado = await self._validate_frete_nao_existe(seller_id, sku)
        if frete_encontrado:
            await self.repository.delete_by_seller_id_and_sku(seller_id, sku)

    def _validate_fretes_positivos(self, frete):
        """
        Valida se os valor de frete é positivo.

        :param frete: Objeto de frete a ser validado.
        :raises BadRequestException: Se o valor do frete for menor que zero.
        """
        valor = getattr(frete, 'valor', getattr(frete, 'valor', None))
        
        if valor is None:
            return
        
        if valor < 0:
            raise BadRequestException(
                details=[ErrorDetail(message="O valor do frete deve ser maior ou igual a zero.", location="body", slug="frete_invalido", field="valor")]
            )

    async def _validate_frete_existe(self, seller_id: str, sku: str):
        """
        Verifica se já existe um frete cadastrado para o seller_id e sku informados.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises BadRequestException: Se já existir frete cadastrado.
        """
        frete_encontrado = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if frete_encontrado is not None:
            raise FreteAlreadyExistsException(message="Frete para produto já cadastrado.", location="body", slug="frete_invalido", field="sku")

    async def _validate_frete_nao_existe(self, seller_id: str, sku: str):
        """
        Verifica se não existe um frete para o seller_id e sku informados.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises FreteNotFoundException: Se não existir frete cadastrado.
        """
        fretes_encontrados = await self.repository.find(
            filters={"seller_id": seller_id, "sku": sku}
        )

        if fretes_encontrados is None:
            raise FreteNotFoundException(
                seller_id=seller_id,
                sku=sku,
            )
        return fretes_encontrados

__all__ = ["FreteService"]