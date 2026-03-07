from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    sessions: Mapped[List["WorkoutSession"]] = relationship(back_populates="user")


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

    notes: Mapped[str|None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")
    sets: Mapped[List["Set"]] = relationship(back_populates="session")


class Set(Base):
    __tablename__ = "sets"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int] = mapped_column(
        ForeignKey("workout_sessions.id"),
        nullable=False
    )

    exercise: Mapped[str] = mapped_column(nullable=False)
    # TODO: Autoincrement set_number based on session_id?
    set_number: Mapped[int] = mapped_column(nullable=True)
    reps: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[int] = mapped_column(server_default="0", nullable=False)
    rest: Mapped[int|None] = mapped_column(nullable=True)

    session: Mapped["WorkoutSession"] = relationship(back_populates="sets")


if __name__ == "__main__":
    engine = create_engine(
        "sqlite:///./workout_tracker.db",
        connect_args={"check_same_thread": False},
        echo=True,
    )
    Base.metadata.create_all(engine)
