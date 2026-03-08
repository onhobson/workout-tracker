from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import WorkoutSession

def get_workout(workout_id: int, db: Session) -> WorkoutSession | None:
    stmt = select(WorkoutSession).where(WorkoutSession.id == workout_id)
    return db.scalar(stmt)


def get_user_workouts(user_id: int, db: Session) -> Sequence[WorkoutSession]:
    stmt = select(WorkoutSession).where(WorkoutSession.user_id == user_id)
    return db.scalars(stmt).all()