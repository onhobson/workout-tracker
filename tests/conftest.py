import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.dependencies import get_current_user
from app.main import app
from app.db.database import get_session
from app.db.models import Base, User

engine = create_engine(
    "sqlite://",
    connect_args={
        "check_same_thread": False,
        "autocommit": False
    },
)

TestSession = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestSession(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session, test_user):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db

    def override_get_current_user():
        yield test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(db_session):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="fakehash"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


