import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import text

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def user_token(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "user@test.pl",
            "password": "User1234!",
        },
    )
    res = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "User1234!"},
    )
    return res.json()["access_token"]


@pytest.fixture()
def admin_token(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "admin",
            "email": "admin@test.pl",
            "password": "Admin123!",
        },
    )
    db = next(override_get_db())
    db.execute(
        text("UPDATE users SET role = 'admin' WHERE username = 'admin'")
    )
    db.commit()
    db.close()
    res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "Admin123!"},
    )
    return res.json()["access_token"]
