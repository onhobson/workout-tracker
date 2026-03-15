from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import EmptyStringError
from app.db.models import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate