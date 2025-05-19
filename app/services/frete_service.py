from uuid import UUID

from ..api.common.schemas.response import ErrorDetail
from ..common.exceptions import BadRequestException, NotFoundException
from ..models import Frete
from ..repositories import FreteRepository
from .base import CrudService


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

    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Frete:
        """
        Busca um fretes pelo seller_id e sku.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :return: Instância de Frete encontrada.
        :raises NotFoundException: Se não encontrar o fretes.
        """
        frete_encontrado = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if frete_encontrado is None:
            self._raise_not_found(seller_id, sku)
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

    async def update_frete_value(self, seller_id: str, sku: str, frete_update: FreteUpdate) -> Frete:
        """
        Atualiza um frete existente com novo valor.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :param frete_update: Objeto contendo o novo valor do frete.
        :return: Instância de Frete atualizada.
        :raises NotFoundException: Se não encontrar o frete.
        :raises BadRequestException: Se valores inválidos forem informados.
        """
        frete_encontrado = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if frete_encontrado is None:
            self._raise_not_found(seller_id, sku)
        self._validate_fretes_positivos(frete_update)
        return await self.update(frete_encontrado.id, {"valor_frete": frete_update.novo_valor_frete})

    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str):
        """
        Remove um frete baseado em seller_id e sku.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises NotFoundException: Se o frete não for encontrado.
        """
        frete_encontrado = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if frete_encontrado is None:
            self._raise_not_found(seller_id, sku)
        await self.repository.delete_by_seller_id_and_sku(seller_id, sku)

    def _validate_fretes_positivos(self, frete):
        """
        Valida se os valor de frete é positivo.

        :param frete: Objeto de frete a ser validado.
        :raises BadRequestException: Se o valor do frete for menor que zero.
        """
        if frete.valor_frete < 0:
            self._raise_bad_request("frete deve ser maior que zero.", "valor_frete")

    async def _validate_frete_nao_existe(self, seller_id: str, sku: str):
        """
        Verifica se já existe um frete cadastrado para o seller_id e sku informados.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises BadRequestException: Se já existir frete cadastrado.
        """
        frete_encontrado = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if frete_encontrado:
            self._raise_bad_request("Frete para produto já cadastrado.", "sku")

    def _raise_not_found(self, seller_id: str, sku: str):
        """
        Lança exceção de NotFoundException com detalhes do erro.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :raises NotFoundException: Sempre.
        """
        raise NotFoundException(
            details=[
                ErrorDetail(
                    message="Frete para produto não encontrado.",
                    location="path",
                    slug="frete_nao_encontrado",
                    field="sku",
                    ctx={"seller_id": seller_id, "sku": sku},
                )
            ]
        )

    def _raise_bad_request(self, message: str, field: str):
        """
        Lança exceção de BadRequestException com detalhes do erro.

        :param message: Mensagem descritiva do erro.
        :param field: Campo relacionado ao erro.
        :raises BadRequestException: Sempre.
        """
        raise BadRequestException(
            details=[ErrorDetail(message=message, location="body", slug="frete_invalido", field=field)]
        )
