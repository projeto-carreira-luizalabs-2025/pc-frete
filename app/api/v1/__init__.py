from fastapi import APIRouter

from app.settings import api_settings

SELLER_V1_PREFIX = "/seller/v1"

router_seller = APIRouter(prefix=SELLER_V1_PREFIX)


def load_routes(router_seller: APIRouter):
    if api_settings.enable_seller_resources:
        from app.api.v1.routers.frete_router import router as frete_router

        router_seller.include_router(frete_router)


load_routes(router_seller)
