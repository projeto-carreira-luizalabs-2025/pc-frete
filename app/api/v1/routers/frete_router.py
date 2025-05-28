from typing import TYPE_CHECKING, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.common.schemas import ListResponse, Paginator, get_request_pagination
from app.container import Container

from ..schemas.frete_schema import FreteCreate, FreteResponse, FreteUpdate
from . import FRETE_PREFIX

if TYPE_CHECKING:
    from app.services import FreteService


router = APIRouter(prefix=FRETE_PREFIX, tags=["Fretes"])

# Busca todos os fretes
@router.get(
    "",
    response_model=ListResponse[FreteResponse],
    status_code=status.HTTP_200_OK,
    summary="Recuperar lista de fretes",
)
@inject
async def get(
    paginator: Paginator = Depends(get_request_pagination),
    seller_id: Optional[str] = None,
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    filters = {}
    if seller_id:
        filters["seller_id"] = seller_id
    results = await frete_service.find_all(paginator=paginator, filters=filters)
    return paginator.paginate(results=results)

# Busca fretes por "seller_id" e "sku"
@router.get(
    "/{seller_id}/{sku}",
    response_model=FreteResponse,
    status_code=status.HTTP_200_OK,
    summary="Recuperar frete por seller_id e sku",
)
@inject
async def get_by_seller_id_and_sku(
    seller_id: str,
    sku: str,
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    return await frete_service.find_by_seller_id_and_sku(seller_id=seller_id, sku=sku)

# Cria um frete para um produto
@router.post(
    "",
    response_model=FreteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um frete para um produto",
)
@inject
async def create(frete: FreteCreate, frete_service: "FreteService" = Depends(Provide[Container.frete_service])):
    return await frete_service.create_frete(frete)

# Atualiza o valor do frete para um produto
@router.patch(
    "/{seller_id}/{sku}",
    response_model=FreteResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar o valor do frete para um produto",
)
@inject
async def update_frete_value(
    seller_id: str,
    sku: str,
    frete_update: FreteUpdate,
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    return await frete_service.update_frete_value(seller_id, sku, frete_update)

# Substitui completamente os dados do frete
@router.put(
    "/{seller_id}/{sku}",
    response_model=FreteResponse,
    status_code=status.HTTP_200_OK,
    summary="Substituir completamente os dados do frete para um produto",
)
@inject
async def replace_frete(
    seller_id: str,
    sku: str,
    frete_data: FreteCreate,
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    return await frete_service.replace_frete(seller_id, sku, frete_data)

# Deleta o frete de um produto
@router.delete(
    "/{seller_id}/{sku}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir frete por seller_id e sku",
)
@inject
async def delete_by_seller_id_and_sku(
    seller_id: str, sku: str, frete_service: "FreteService" = Depends(Provide[Container.frete_service])
):
    await frete_service.delete_by_seller_id_and_sku(seller_id, sku)
