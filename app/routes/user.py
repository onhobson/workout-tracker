from fastapi import APIRouter, HTTPException, status

from app.crud import user as crud_user
from app.dependencies import *
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UserRead)
def get_user(user: CurrentUser, db: DbSession):
    user_found = crud_user.get_user(user.id, db)

    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user_found