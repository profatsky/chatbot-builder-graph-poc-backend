from fastapi import HTTPException, status


class ButtonNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Button not found',
        )


class IncorrectNumberOfButtonsHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Incorrect number of buttons',
        )


class ButtonIdsMismatchHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Button ids mismatch',
        )


class IncorrectButtonSeqNumbersHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Incorrect button sequence numbers',
        )
