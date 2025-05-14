from fastapi import HTTPException, status


class ActionNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Action not found',
        )


class IncorrectNumberOfActionsHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Incorrect number of actions',
        )


class ActionIdsMismatchHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Action ids mismatch',
        )


class IncorrectActionSeqNumbersHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect action sequence numbers',
        )


class IncorrectActionTypeHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect action type',
        )
