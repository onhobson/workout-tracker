from app.db.database import engine
from app.db.models import Base

def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    reset_db()