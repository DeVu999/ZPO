from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, items, users
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(User).filter(User.username == "admin").first():
        db.add(
            User(
                username="admin",
                email="admin@admin.pl",
                hashed_password=hash_password("Admin123!"),
                role="admin",
            )
        )
        db.commit()
    db.close()
    yield


app = FastAPI(title="Projekt1", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
