from uuid import UUID

from ...api.common.schemas.response import ErrorDetail
from ...common.exceptions import BadRequestException, NotFoundException
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

        :param paginator: Objeto de paginação para controlar os resultados.
        :param filters: Dicionário de filtros para aplicar na busca (seller_id).
        :return: Lista de instâncias de Frete encontradas.
        """
        return await self.repository.find_all(paginator=paginator, filters=filters)
    
    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Frete:
        """
        Busca um fretes pelo seller_id e sku.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :return: Instância de Frete encontrada.
        :raises FreteNotFoundException: Se não encontrar o frete.
        """
        frete_encontrado = await self._validate_frete_encontrado(seller_id, sku)
        return frete_encontrado

    async def create_frete(self, frete_create) -> Frete:
        """
        Cria uma novo frete após validações de unicidade e valores positivos.

        :param frete_create: Objeto contendo os dados para criação do fretes.
        :return: Instância de Frete criada.
        :raises BadRequestException: Se já existir fretes para o produto ou valores inválidos.
        """
        await self._validate_frete_nao_existe(frete_create.seller_id, frete_create.sku)
        self._validate_fretes_positivos(frete_create)
        # Converte FreteCreate para Frete, gerando o id automaticamente
        frete = Frete(**frete_create.model_dump())
        return await self.create(frete)

    async def update_frete_value(self, seller_id: str, sku: str, frete_update) -> Frete:
        """
        Atualiza um frete existente com novo valor.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :param frete_update: Objeto contendo o novo valor do frete.
        :return: Instância de Frete atualizada.
        :raises NotFoundException: Se não encontrar o frete.
        :raises BadRequestException: Se valores inválidos forem informados.
        """
        frete_existente = await self._validate_frete_encontrado(seller_id, sku)

        self._validate_fretes_positivos(frete_update)
    
        # Cria um dicionário com apenas o campo a ser atualizado
        frete_atualizado = {
            "seller_id": seller_id,
            "sku": sku,
            "valor": frete_update.valor
        }
        
        # Usa o ID do dicionário
        return await self.update(frete_existente["_id"], frete_atualizado)

    async def replace_frete(self, seller_id: str, sku: str, frete_update) -> Frete:
        """
        Substitui completamente os dados de um frete existente.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :param frete_update: Objeto contendo os dados atualizados.
        :return: Instância de Frete atualizada.
        :raises FreteNotFoundException: Se não encontrar o frete.
        :raises BadRequestException: Se os dados forem inválidos.
        """
        frete_existente = await self._validate_frete_encontrado(seller_id, sku)

        self._validate_fretes_positivos(frete_update)

        frete_dict = frete_update.model_dump()

        frete_dict["seller_id"] = frete_update.seller_id
        frete_dict["valor"] = frete_update.valor
        frete_dict["sku"] = frete_update.sku

        return await self.update(frete_existente["_id"], frete_dict)


    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str):
        """
        Remove um frete baseado em seller_id e sku.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises NotFoundException: Se o frete não for encontrado.
        """
        await self._validate_frete_encontrado(seller_id, sku)
        await self.repository.delete_by_seller_id_and_sku(seller_id, sku)

    def _validate_fretes_positivos(self, frete):
        """
        Valida se os valor de frete é positivo.

        :param frete: Objeto de frete a ser validado.
        :raises BadRequestException: Se o valor do frete for menor que zero.
        """
        valor = getattr(frete, 'valor', getattr(frete, 'valor', None))
    
        if valor is None:
            raise BadRequestException(
                details=[ErrorDetail(message="Valor do frete não especificado.", location="body", slug="frete_invalido", field="valor")]
            )
            
        if valor < 0:
            raise BadRequestException(
                details=[ErrorDetail(message="frete deve ser maior que zero.", location="body", slug="frete_invalido", field="valor")]
            )

    async def _validate_frete_nao_existe(self, seller_id: str, sku: str):
        """
        Verifica se já existe um frete cadastrado para o seller_id e sku informados.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises BadRequestException: Se já existir frete cadastrado.
        """
        frete_encontrado = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if frete_encontrado:
            raise FreteAlreadyExistsException(message="Frete para produto já cadastrado.", location="body", slug="frete_invalido", field="sku")

    async def _validate_frete_encontrado(self, seller_id: str, sku: str):
        """
        Verifica se existe um frete para o seller_id e sku informados.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises FreteNotFoundException: Se não existir frete cadastrado.
        """
        frete_encontrado = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if not frete_encontrado:
            raise FreteNotFoundException(
                seller_id=seller_id,
                sku=sku,
            )
        return frete_encontrado

__all__ = ["FreteService"]