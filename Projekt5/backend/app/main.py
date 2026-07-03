from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, employees, users
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.employee import Employee
from app.models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if not db.query(User).filter(User.username == "admin").first():
        db.add(User(
            username="admin", email="admin@admin.pl",
            hashed_password=hash_password("Admin123!"), role="admin",
        ))
        db.commit()

    if not db.query(User).filter(User.username == "test").first():
        db.add(User(
            username="test", email="test@test.pl",
            hashed_password=hash_password("Test1234!"), role="user",
        ))
        db.commit()

    if not db.query(Employee).filter(Employee.name == "Jan Kowalski").first():
        emp = Employee(name="Jan Kowalski", position="Kierownik", department="IT")
        db.add(emp)
        db.commit()

    db.close()
    yield


app = FastAPI(title="ZarzadzaniePracownikami", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(employees.router)