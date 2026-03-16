"""
CRUD operations for users.
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
    Retrieve a user by ID.
    Returns None if the user does not exist.
    """
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Retrieve a user by username.
    Returns None if the user does not exist.
    """
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def create_user(user: UserCreate, db: Session) -> User | None:
    """
    Create a new user with the provided data.

    Args:
        user: UserCreate data for the new user, including username, email, and password.
        db: Database session for querying and committing the new user.
    Returns:
        The created User object if successful, or None if there was an error during creation.
    Raises:
        EmptyStringError: If any of the required fields are empty strings.
        DuplicateUserError: If the username or email already exists in the database.
    """
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
    """
    Update an existing user's information with the provided data.

    Args:
        user_data: UserUpdate data containing the fields to update, such as username, email, or password.
        user: The existing User object to be updated.
        db: Database session for querying and committing the updated user.
    Returns:
        The updated User object if successful, or None if there was an error during the update.
    Raises:
        EmptyStringError: If any of the updated fields are empty strings.
    """
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
    """
    Delete a user by ID.
    Returns True if the user was deleted, False if the user does not exist.
    """
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)

    if not user:
        return False
    
    db.delete(user)
    db.commit()

    return True