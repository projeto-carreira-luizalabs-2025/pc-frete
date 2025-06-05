from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Header, HTTPException

from app.api.common.schemas import ListResponse, Paginator, get_request_pagination
from app.container import Container

from ..schemas.frete_schema import FreteSchema, FreteResponse, FreteCreate, FreteCreateResponse, FreteUpdate, FreteUpdateResponse, FreteReplace, FreteReplaceResponse
from . import FRETE_PREFIX

if TYPE_CHECKING:
    from app.services import FreteService


router = APIRouter(prefix=FRETE_PREFIX, tags=["Fretes V2"])

async def get_seller_id(x_seller_id: str = Header(..., alias="x-seller-id")) -> str:
    if not x_seller_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cabeçalho x-seller-id é obrigatório")
    return x_seller_id

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
    seller_id: str = Depends(get_seller_id),
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    filters = {"seller_id": seller_id}
    results = await frete_service.find_all(paginator=paginator, filters=filters)
    return paginator.paginate(results=results)

# Busca fretes por "seller_id" e "sku"
@router.get(
    "/{sku}",
    response_model=FreteResponse,
    status_code=status.HTTP_200_OK,
    summary="Recuperar frete por seller_id e sku",
)
@inject
async def get_by_seller_id_and_sku(
    sku: str,
    seller_id: str = Depends(get_seller_id),
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    return await frete_service.find_by_seller_id_and_sku(seller_id=seller_id, sku=sku)

# Cria um frete para um produto
@router.post(
    "",
    response_model=FreteCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um frete para um produto",
)
@inject
async def create(
    novo_frete: FreteCreate,
    seller_id: str = Depends(get_seller_id),
    frete_service: "FreteService" = Depends(Provide[Container.frete_service])
):
    frete = FreteSchema(seller_id=seller_id, sku=novo_frete.sku, valor=novo_frete.valor)
    return await frete_service.create_frete(frete)

# Atualiza os dados informados de um frete para um produto
@router.patch(
    "/{sku}",
    response_model=FreteUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar os dados informados de um frete para um produto",
)
@inject
async def update_frete_value(
    sku: str,
    frete_data: FreteUpdate,
    seller_id: str = Depends(get_seller_id),
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    return await frete_service.update_frete_value(seller_id, sku, frete_data)

# Substitui completamente os dados do frete
@router.put(
    "/{sku}",
    response_model=FreteReplaceResponse,
    status_code=status.HTTP_200_OK,
    summary="Substituir completamente os dados do frete para um produto",
)
@inject
async def replace_frete(
    sku: str,
    frete_data: FreteReplace,
    seller_id: str = Depends(get_seller_id),
    frete_service: "FreteService" = Depends(Provide[Container.frete_service]),
):
    return await frete_service.replace_frete(seller_id, sku, frete_data)

# Deleta o frete de um produto
@router.delete(
    "/{sku}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir frete por sku",
)
@inject
async def delete_by_seller_id_and_sku(
    sku: str, 
    seller_id: str = Depends(get_seller_id), 
    frete_service: "FreteService" = Depends(Provide[Container.frete_service])
):
    await frete_service.delete_by_seller_id_and_sku(seller_id, sku)
