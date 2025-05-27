from app.api.common.schemas.response import ErrorDetail
from app.common.exceptions import ConflictException, NotFoundException

class FreteAlreadyExistsException(ConflictException):
    def __init__(
        self,
        message: str,
        location: str,
        slug: str,
        field: str,
    ):
        details = [
            ErrorDetail(
                message=message,
                location=location,
                slug=slug,
                field=field,
            )
        ]
        super().__init__(details=details)

class FreteNotFoundException(NotFoundException):
    def __init__(
        self,
        seller_id: str,
        sku: str,
    ):
        details = [
            ErrorDetail(
                message="Frete para produto não encontrado.",
                location="path",
                slug="frete_nao_encontrado",
                field="sku",
                ctx={"seller_id": seller_id, "sku": sku},
            )
        ]
        super().__init__(details=details)