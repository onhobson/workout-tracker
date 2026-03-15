from app.routes.auth import router as auth_router
from app.routes.equipment import router as equipment_router
from app.routes.workout import router as workout_router
from app.routes.set import router as set_router
from app.routes.user import router as user_router

routers = [
    auth_router,
    equipment_router,
    workout_router,
    set_router,
    user_router,
]