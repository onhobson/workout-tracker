from fastapi import APIRouter

from app.crud import user as crud_user
from app.dependencies import *
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserRead)
def get_user(user: CurrentUser, db: DbSession):
    return crud_user.get_user(user.id, db)