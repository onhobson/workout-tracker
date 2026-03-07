from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///./workout_tracker.db",
    connect_args={"check_same_thread": False},
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_session():
    with Session.begin() as session:
        yield session