from app.routes.user import router as user_router
from app.routes.workout import router as workout_router
from app.routes.set import router as set_router

routers = [
    user_router,
    workout_router,
    set_router,
]