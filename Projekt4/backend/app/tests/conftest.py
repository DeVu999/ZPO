import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    from app.models.user import User
    admin_user = db.query(User).filter(User.username == "admin").first()
    admin_user.role = "admin"
    db.commit()
    db.close()
    res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "Admin123!"},
    )
    return res.json()["access_token"]


@pytest.fixture()
def user2_token(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "user2",
            "email": "user2@test.pl",
            "password": "Test1234!",
        },
    )
    res = client.post(
        "/api/auth/login",
        data={"username": "user2", "password": "Test1234!"},
    )
    return res.json()["access_token"]


@pytest.fixture()
def sample_class(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.post(
        "/api/classes",
        json={
            "name": "Test Fitness",
            "description": "Opis testowy",
            "instructor": "Trener Test",
            "datetime": "2026-08-01T10:00:00",
            "capacity": 2,
        },
        headers=headers,
    )
    return res.json()


@pytest.fixture()
def full_class(client, admin_token, user_token, user2_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.post(
        "/api/classes",
        json={
            "name": "Pelne Zajecia",
            "description": "Test waitlisty",
            "instructor": "Trener Full",
            "datetime": "2026-08-02T10:00:00",
            "capacity": 2,
        },
        headers=headers,
    )
    class_data = res.json()

    ht = {"Authorization": f"Bearer {user_token}"}
    h2 = {"Authorization": f"Bearer {user2_token}"}
    client.post(f"/api/classes/{class_data['id']}/signup", headers=ht)
    client.post(f"/api/classes/{class_data['id']}/signup", headers=h2)

    return class_data
