from . import PersistableEntity


class Frete(PersistableEntity):
    seller_id: str
    sku: str
    valor_frete: int
