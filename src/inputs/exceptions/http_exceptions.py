from fastapi import status, HTTPException


class InputNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Input not found',
        )


class InputTypeConflictHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Input with this type already exists in the group',
        )
