from fastapi import APIRouter, HTTPException, status

from app.crud import exercise as crud_exercise
from app.dependencies import *
from app.schemas.exercise import ExerciseCreate, ExerciseRead, ExerciseUpdate

router = APIRouter(prefix="/exercises", tags=["Exercises"])
