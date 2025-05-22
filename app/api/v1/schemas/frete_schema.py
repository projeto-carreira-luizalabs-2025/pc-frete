from app.api.common.schemas import ResponseEntity, SchemaType
from pydantic import Field

class FreteSchema(SchemaType):
    seller_id: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    valor_frete: int

class FreteResponse(FreteSchema, ResponseEntity):
    """Resposta adicionando"""

class FreteCreate(FreteSchema):
    """Schema para criação de Fretes"""

class FreteUpdate(SchemaType):
    """Schema para atualização de Fretes"""
    novo_valor_frete: int
