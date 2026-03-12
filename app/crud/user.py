from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(user_id: int, db: Session) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def create_user(user: UserCreate, db: Session) -> User | None:
    user.username = user.username.lower()
    user.email = user.email.lower()
    user.password = hash_password(user.password)

    new_user = User(
        **user.model_dump()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(user_data: UserUpdate, user_id: int, db: Session) -> User | None:
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)

    if not user:
        return None
    
    if user_data.password is not None:
        user_data.password = hash_password(user_data.password)

    if user_data.username is not None:
        user_data.username = user_data.username.lower()

    if user_data.email is not None:
        user_data.email = user_data.email.lower()

    update_data = user_data.model_dump(exclude_unset=True)
    
    for column, value in update_data.items():
        setattr(user, column, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(user_id: int, db: Session) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)

    if not user:
        return False
    
    db.delete(user)
    db.commit()

    return True