from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import User


def get_user(user_id: int, db: Session) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)