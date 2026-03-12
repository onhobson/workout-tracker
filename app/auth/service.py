from app.dependencies import *
from app.crud import user as crud_user
from app.auth.hashing import verify_password, verify_password_dummy
from app.db.models import User


def authenticate_user(
        db: DbSession,
        username: str,
        password: str,
) -> User | None:
    username = username.lower()

    user = crud_user.get_user_by_username(db, username)

    if not user:
        verify_password_dummy(password)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user