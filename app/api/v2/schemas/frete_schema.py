from app.api.common.schemas import ResponseEntity, SchemaType
from pydantic import Field

class FreteBase(SchemaType):
    seller_id: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)

class FreteSchema(FreteBase):
    valor: int

class FreteResponse(FreteSchema, ResponseEntity):
    """Resposta adicionando"""

class FreteCreate(SchemaType):
    """Schema para criação de Fretes"""
    sku: str = Field(..., min_length=1)
    valor: int

class FreteCreateResponse(FreteBase):
    """Resposta para a criação de Fretes"""

class FreteUpdate(SchemaType):
    """Schema para atualização de Fretes"""
    seller_id: str | None = Field(default=None, min_length=1)
    sku: str | None = Field(default=None, min_length=1)
    valor: int | None = Field(default=None)

class FreteUpdateResponse(FreteBase):
    """Resposta para a atualização de Fretes"""

class FreteReplace(SchemaType):   
    """Schema para substituição de Fretes"""
    seller_id: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    valor: int

class FreteReplaceResponse(FreteBase):
    """Resposta para a substituição de Fretes"""