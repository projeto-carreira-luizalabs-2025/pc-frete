from app.api.common.schemas.response import ErrorDetail
from app.common.exceptions import ConflictException

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
