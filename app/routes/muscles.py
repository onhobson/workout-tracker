from fastapi import APIRouter, HTTPException, status

from app.crud import muscles as crud_muscles
from app.dependencies import *
from app.schemas.muscles import MuscleGroupRead, MuscleGroupWithExercises

router = APIRouter(prefix="/sets", tags=["Sets"])
