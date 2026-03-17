from fastapi import FastAPI
import uvicorn

from app.db.models import Base
from app.db.database import engine
from app.routes import routers

app = FastAPI()

Base.metadata.create_all(bind=engine)


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)