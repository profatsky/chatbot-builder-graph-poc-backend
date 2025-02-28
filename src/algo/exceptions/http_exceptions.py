from fastapi import HTTPException, status


class GroupNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )
