from fastapi import HTTPException, status
from pydantic import BaseModel


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
