from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.exceptions import UnauthorizedException
from src.schemas import Token, User
from src.services.user import UserService
from src.settings import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 4320


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/form_token")
access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(email: str) -> Token:
    to_encode = {"sub": email, "exp": datetime.utcnow() + access_token_expires}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], user_service: UserService = Depends()
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise UnauthorizedException
    except JWTError:
        raise UnauthorizedException
    user = await user_service.get_by_email(username)
    if user is None:
        raise UnauthorizedException
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user
