from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MuscleGroup


def get_all_muscle_groups(db: Session) -> Sequence[MuscleGroup]:
    return db.scalars(select(MuscleGroup)).all()


def get_muscle_group(muscle_id: int, db: Session) -> MuscleGroup | None:
    stmt = select(MuscleGroup).where(MuscleGroup.id == muscle_id)
    return db.scalar(stmt)