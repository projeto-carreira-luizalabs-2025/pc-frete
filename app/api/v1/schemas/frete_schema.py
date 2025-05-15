from app.api.common.schemas import ResponseEntity, SchemaType


class FreteSchema(SchemaType):
    seller_id: str
    sku: str
    valor_frete: int


class FreteResponse(FreteSchema, ResponseEntity):
    """Resposta adicionando"""


class FreteCreate(FreteSchema):
    """Schema para criação Fretes"""
