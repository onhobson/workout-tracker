from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Set, WorkoutSession
from app.schemas.set import SetCreate, SetUpdate

def get_set(set_id: int, user_id: int, db: Session) -> Set | None:
    stmt = (
        select(Set)
        .join(WorkoutSession)
        .where(
            Set.id == set_id,
            WorkoutSession.user_id == user_id
        )
    )
    return db.scalar(stmt)


def create_set(set_data: SetCreate, db: Session) -> Set | None:
    workout_set = Set(
        **set_data.model_dump(),
    )

    db.add(workout_set)
    db.commit()
    db.refresh(workout_set)

    return workout_set


def update_set(
    set_id: int, 
    set_data: SetUpdate, 
    user_id: int, 
    db: Session
) -> Set | None:
    stmt = (
        select(Set)
        .join(WorkoutSession)
        .where(
            Set.id == set_id, 
            WorkoutSession.user_id == user_id
        )
    )

    workout_set = db.scalar(stmt)

    if not workout_set:
        return None

    update_data = set_data.model_dump(exclude_unset=True)

    for column, value in update_data.items():
        setattr(workout_set, column, value)
    
    db.commit()
    db.refresh(workout_set)

    return workout_set


def delete_set(set_id: int, user_id: int, db: Session) -> bool:
    stmt = (
        select(Set)
        .join(WorkoutSession)
        .where(
            Set.id == set_id, 
            WorkoutSession.user_id == user_id
        )
    )

    workout_set = db.scalar(stmt)

    if not workout_set:
        return False
    
    db.delete(workout_set)
    db.commit()

    return True