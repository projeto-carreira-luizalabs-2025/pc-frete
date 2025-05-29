from fastapi import APIRouter

from app.settings import api_settings

SELLER_V2_PREFIX = "/seller/v2"

router_selller = APIRouter(prefix=SELLER_V2_PREFIX)


def load_routes(router_seller: APIRouter):
    if api_settings.enable_seller_resources:
        from app.api.v2.routers.frete_router import router as frete_router

        router_seller.include_router(frete_router)


load_routes(router_selller)
