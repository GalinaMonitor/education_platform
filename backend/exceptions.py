from fastapi import HTTPException, status
from pydantic import BaseModel
from starlette import status


class Error(BaseModel):
    code: int
    message: str


class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AlreadyRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
            headers={"WWW-Authenticate": "Bearer"},
        )


class HasNoSubscriptionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No subscription",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
