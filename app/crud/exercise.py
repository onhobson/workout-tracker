"""
CRUD operations for exercises.
"""
from typing import Sequence

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.core.exceptions import EmptyStringError, InvalidForeignKeyIDError
from app.db.models import Equipment, Exercise, ExerciseMuscleGroup, MuscleGroup
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


def get_exercises(
    muscle_id: int | None, 
    equipment_id: int | None,
    user_id: int,
    db: Session
) -> Sequence[Exercise]:
    """
    Retrieve exercises filtered by muscle group, equipment, and user.

    Args:
        muscle_id: Optional muscle group ID to filter exercises that target a specific muscle group.
        equipment_id: Optional equipment ID to filter exercises that use specific equipment.
        user_id: ID of the user making the request, used to include user-created exercises.
        db: Database session for querying.
    Returns:
        A sequence of Exercise objects matching the specified filters.
    """
    stmt = select(Exercise).where(
        or_(
            Exercise.created_by_user_id.is_(None),
            Exercise.created_by_user_id == user_id
        )
    )

    if equipment_id:
        stmt = stmt.where(
            Exercise.equipment_id == equipment_id
        )
    
    if muscle_id:
        stmt = stmt.join(ExerciseMuscleGroup).where(
            ExerciseMuscleGroup.muscle_group_id == muscle_id
        )

    return db.scalars(stmt).all()


def get_exercise(exercise_id: int, user_id: int, db: Session) -> Exercise | None:
    """Retrieve a specific exercise by ID, ensuring it is either a default exercise or created by the user."""
    stmt = (
        select(Exercise)
        .where(
            Exercise.id == exercise_id,
            or_(
                Exercise.created_by_user_id.is_(None),
                Exercise.created_by_user_id == user_id
            )
        )
    )

    return db.scalar(stmt)


def create_exercise(exercise_data: ExerciseCreate, user_id: int, db: Session) -> Exercise:
    """
    Create a new exercise with the provided data, ensuring all referenced IDs are valid and required fields are not empty.
    
    Args:
        exercise_data: ExerciseCreate object containing the data for the new exercise.
        user_id: ID of the user creating the exercise, used to set the created_by_user_id field.
        db: Database session for querying and committing the new exercise.
    Returns:
        The newly created Exercise object.
    Raises:
        EmptyStringError: If any required string fields are empty.
        InvalidForeignKeyIDError: If any foreign key IDs do not correspond to existing records in the database.
    """
    if exercise_data.name.strip() == "":
        raise EmptyStringError("name")

    for muscle in exercise_data.muscle_groups:
        if not db.get(MuscleGroup, muscle.muscle_group_id):
            raise InvalidForeignKeyIDError(f"muscle_group_id: {muscle.muscle_group_id}")
        if muscle.role.strip() == "":
            raise EmptyStringError("role")
    
    if not db.get(Equipment, exercise_data.equipment_id):
        raise InvalidForeignKeyIDError(f"equipment_id: {exercise_data.equipment_id}")
 
    exercise = Exercise(
        name=exercise_data.name,
        equipment_id=exercise_data.equipment_id,
        created_by_user_id=user_id,
    )

    db.add(exercise)
    db.flush()

    for muscle in exercise_data.muscle_groups:
        exercise.muscles.append(
            ExerciseMuscleGroup(
                muscle_group_id=muscle.muscle_group_id,
                role=muscle.role,
            )
        )

    db.commit()
    db.refresh(exercise)

    return exercise


def update_exercise(exercise_id: int, exercise_data: ExerciseUpdate, user_id: int, db: Session) -> Exercise | None: 
    """
    Update an existing exercise with the provided data, ensuring the exercise belongs to the user and all referenced IDs are valid.
    
    Args:
        exercise_id: ID of the exercise to update.
        exercise_data: ExerciseUpdate object containing the updated data for the exercise.
        user_id: ID of the user updating the exercise, used to verify ownership.
        db: Database session for querying and committing the updated exercise.
    Returns:
        The updated Exercise object if the update was successful, or None if the exercise does not exist or does not belong to the user.
    Raises:
        EmptyStringError: If any required string fields are empty.
        InvalidForeignKeyIDError: If any foreign key IDs do not correspond to existing records in the database.
    """
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.created_by_user_id == user_id
    )

    exercise = db.scalar(stmt)

    if not exercise:
        return None
    
    if exercise_data.muscle_groups:
        for muscle in exercise_data.muscle_groups:
            if not db.get(MuscleGroup, muscle.muscle_group_id):
                raise InvalidForeignKeyIDError(f"muscle_group_id: {muscle.muscle_group_id}")
            if muscle.role.strip() == "":
                raise EmptyStringError("role")
    
    if exercise_data.equipment_id and not db.get(Equipment, exercise_data.equipment_id):
        raise InvalidForeignKeyIDError(f"equipment_id: {exercise_data.equipment_id}")

    
    if exercise_data.name:
        exercise.name = exercise_data.name

    if exercise_data.equipment_id:
        exercise.equipment_id = exercise_data.equipment_id

    if exercise_data.muscle_groups:
        exercise.muscles.clear()

        for muscle in exercise_data.muscle_groups:
            exercise.muscles.append(
                ExerciseMuscleGroup(
                    muscle_group_id=muscle.muscle_group_id,
                    role=muscle.role
                )
            )

    db.commit()
    db.refresh(exercise)

    return exercise


def delete_exercise(exercise_id: int, user_id: int, db: Session) -> bool:
    """
    Delete an exercise by ID, ensuring it belongs to the user.
    Returns True if the exercise was deleted, False if the exercise does not exist or does not belong to the user.
    """
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.created_by_user_id == user_id
    )

    exercise = db.scalar(stmt)

    if not exercise:
        return False
    
    db.delete(exercise)
    db.commit()

    return True