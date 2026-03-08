from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.user import get_user
from app.db.database import  get_session
from app.db.models import User


def get_current_user(token: str, db: Annotated[Session, Depends(get_session)]):
    user = get_user(1, db)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]