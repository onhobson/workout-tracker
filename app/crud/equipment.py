from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Equipment


def get_all_equipment(db: Session) -> Sequence[Equipment]:
    return db.scalars(select(Equipment)).all()


def get_equipment(equipment_id: int, db: Session) -> Equipment | None:
    stmt = select(Equipment).where(Equipment.id == equipment_id)
    return db.scalar(stmt)