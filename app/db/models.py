from datetime import datetime
from typing import List

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, UniqueConstraint, create_engine, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import app.core.limits as LIMIT
from app.db.constraints import range_constraint

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(f"LENGTH(username) >= {LIMIT.USERNAME_MIN_LENGTH}", "chk_username_min"),
        CheckConstraint(f"LENGTH(email) >= {LIMIT.EMAIL_MIN_LENGTH}", "chk_email_min"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(LIMIT.USERNAME_MAX_LENGTH),
        unique=True, 
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(LIMIT.EMAIL_MAX_LENGTH),
        unique=True, 
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    workouts: Mapped[List["WorkoutSession"]] = relationship(back_populates="user")


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(LIMIT.WORKOUT_NAME_MAX_LENGTH),
        nullable=False,
    )
    notes: Mapped[str|None] = mapped_column(
        String(LIMIT.NOTES_MAX_LENGTH),
        nullable=True,
    )

    user: Mapped["User"] = relationship(back_populates="workouts")
    sets: Mapped[List["Set"]] = relationship(back_populates="workout")


class Set(Base):
    __tablename__ = "sets"
    __table_args__ = (
        range_constraint("workout_id", 0, name="chk_set_workout_id_min"),
        range_constraint("exercise_id", 0, name="chk_set_exercise_id_min"),
        range_constraint("reps", LIMIT.REPS_MIN, LIMIT.REPS_MAX, "chk_set_reps_range"),
        range_constraint("weight", LIMIT.WEIGHT_MIN, LIMIT.WEIGHT_MAX, "chk_set_weight_range"),
        range_constraint("rest", LIMIT.REST_MIN, LIMIT.REST_MAX, "chk_set_rest_range"),
        UniqueConstraint("workout_id", "exercise_id", "set_number", name="uq_exercise_set_per_workout"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workout_sessions.id"),
        nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id"),
        nullable=False,
    )

    set_number: Mapped[int] = mapped_column(nullable=False)
    reps: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[int] = mapped_column(server_default="0", nullable=False)
    rest: Mapped[int|None] = mapped_column(nullable=True)

    workout: Mapped["WorkoutSession"] = relationship(back_populates="sets")
    exercise: Mapped["Exercise"] = relationship()
    

class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = (
        range_constraint("equipment_id", 0, name="chk_exercise_equipment_id_min"),
        CheckConstraint("LENGTH(name) >= 0", "chk_exercise_name_min"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"),
        nullable=False,
    )
    created_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(LIMIT.EXERCISE_NAME_MAX_LENGTH),
        nullable=False,
    )

    equipment: Mapped["Equipment"] = relationship()
    muscles: Mapped[List["ExerciseMuscleGroup"]] = relationship(back_populates="exercise")


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    input_mode: Mapped[str] = mapped_column(nullable=False)


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)

    exercises: Mapped[List["ExerciseMuscleGroup"]] = relationship(back_populates="muscle")


class ExerciseMuscleGroup(Base):
    __tablename__ = "exercise_muscle_groups"

    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id"),
        primary_key=True,
    )
    muscle_group_id: Mapped[int] = mapped_column(
        ForeignKey("muscle_groups.id"),
        primary_key=True,
    )

    role: Mapped[str] = mapped_column(nullable=False)

    exercise: Mapped["Exercise"] = relationship(back_populates="muscles")
    muscle: Mapped["MuscleGroup"] = relationship(back_populates="exercises")


if __name__ == "__main__":
    engine = create_engine(
        "sqlite:///./workout_tracker.db",
        connect_args={"check_same_thread": False},
        echo=True,
    )
    Base.metadata.create_all(engine)
