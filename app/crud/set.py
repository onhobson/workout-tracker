from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Set

def get_set(set_id: int, db: Session) -> Set | None:
    stmt = select(Set).where(Set.id == set_id)
    return db.scalar(stmt)


def get_set_by_workout(workout_id: int, db: Session) -> Sequence[Set]:
    stmt = select(Set).where(Set.workout_id == workout_id)
    return db.scalars(stmt).all()