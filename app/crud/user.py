from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.user import UserCreate


def get_user(user_id: int, db: Session) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def create_user(user: UserCreate, db: Session) -> User | None:
    new_user = User(
        **user.model_dump()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user