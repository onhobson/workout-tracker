"""
Database operations related to users.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.auth.hashing import hash_password
from app.core.exceptions import DuplicateUserError, EmptyStringError
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.normalization import normalize_user_info


def get_user(user_id: int, db: Session) -> User | None:
    """
    Return user by ID.
    """
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Return user by username.
    """
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def create_user(user: UserCreate, db: Session) -> User | None:
    user_data = user.model_dump()

    user_data = normalize_user_info(user_data)

    for field, value in user_data.items():
        if not value.strip():
            raise EmptyStringError(field)
    
    user_data["hashed_password"] = hash_password(
        user_data.pop("password")
    )

    new_user = User(
        **user_data
    )

    db.add(new_user)

    try:
        db.flush()
    except IntegrityError as e:
        db.rollback()

        if "username" in str(e.orig):
            raise DuplicateUserError("username")
        if "email" in str(e.orig):
            raise DuplicateUserError("email")

    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(user_data: UserUpdate, user: User, db: Session) -> User | None:
    update_data = user_data.model_dump(exclude_unset=True)

    update_data = normalize_user_info(update_data)

    for field, value in update_data.items():
        if not value.strip():
            raise EmptyStringError(field)
    
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(
            update_data.pop("password")
        )
    
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