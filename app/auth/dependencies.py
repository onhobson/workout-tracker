from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.auth.jwt import decode_access_token
from app.crud.user import get_user_by_username
from app.db.models import User
from app.dependencies import DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DbSession,
):
    """
    Decode JWT token and return authenticated user.

    Raises HTTPException(401) if token is invalid or user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user_by_username(db, username)

    if user is None:
        raise credentials_exception
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]