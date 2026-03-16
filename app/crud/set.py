"""
CRUD operations for sets.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Set, WorkoutSession
from app.schemas.set import SetCreate, SetUpdate

def get_set(set_id: int, user_id: int, db: Session) -> Set | None:
    """
    Retrieve a specific set by ID, ensuring it belongs to the user.
    Return None if the set does not exist or does not belong to the user.
    """
    stmt = (
        select(Set)
        .join(WorkoutSession)
        .where(
            Set.id == set_id,
            WorkoutSession.user_id == user_id
        )
    )
    return db.scalar(stmt)


def create_set(set_data: SetCreate, user_id: int, db: Session) -> Set | None:
    """
    Create a new set for a workout session, ensuring the workout belongs to the user.

    Args:
        set_data: SetCreate data for the new set, including workout_id and exercise_id.
        user_id: ID of the user creating the set.
        db: Database session for querying and committing the new set.
    Returns:
        The created Set object if successful, or None if the workout does not belong to the user.
    """
    stmt = select(WorkoutSession).where(WorkoutSession.id == set_data.workout_id)
    workout = db.scalar(stmt)

    if not workout:
        return None
    
    if workout.user_id != user_id:
        return None
    
    stmt = (
        select(func.max(Set.set_number))
        .where(
            Set.workout_id == set_data.workout_id,
            Set.exercise_id == set_data.exercise_id,
        )
    )
    current_max = db.scalar(stmt)

    next_set_number = 1 if current_max is None else current_max + 1

    workout_set = Set(
        set_number = next_set_number,
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
    """
    Update an existing set, ensuring it belongs to the user.
    Args:
        set_id: ID of the set to update.
        set_data: SetUpdate data containing the fields to update.
        user_id: ID of the user updating the set, used to verify ownership.
        db: Database session for querying and committing the updated set.
    Returns:
        The updated Set object if successful, or None if the set does not exist or does not belong to the user.
    """
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
    """
    Delete a specific set by ID, ensuring it belongs to the user.
    Returns True if the set was deleted, False if it does not exist or does not belong to the user.
    """
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