from . import SelllerSkuUuidPersistableEntity


class Frete(SelllerSkuUuidPersistableEntity):
    seller_id: str
    sku: str
    valor: int
