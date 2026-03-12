from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
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

    name: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str|None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="workouts")
    sets: Mapped[List["Set"]] = relationship(back_populates="workout")


class Set(Base):
    __tablename__ = "sets"
    __table_args__ = (
        UniqueConstraint("workout_id", "exercise", "set_number", name="uq_exercise_set_per_workout"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workout_sessions.id"),
        nullable=False
    )

    exercise: Mapped[str] = mapped_column(nullable=False)
    set_number: Mapped[int] = mapped_column(nullable=False)
    reps: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[int] = mapped_column(server_default="0", nullable=False)
    rest: Mapped[int|None] = mapped_column(nullable=True)

    workout: Mapped["WorkoutSession"] = relationship(back_populates="sets")


if __name__ == "__main__":
    engine = create_engine(
        "sqlite:///./workout_tracker.db",
        connect_args={"check_same_thread": False},
        echo=True,
    )
    Base.metadata.create_all(engine)
