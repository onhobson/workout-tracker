from fastapi import APIRouter

from app.crud import set as crud_set
from app.dependencies import *
from app.schemas.set import SetRead

router = APIRouter(prefix="/sets", tags=["Sets"])


@router.get("/{set_id}", response_model=SetRead)
def get_set(set_id: int, db: DbSession):
    return crud_set.get_set(set_id, db)