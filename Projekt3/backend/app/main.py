from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, rooms, users
from app.api.rooms import bookings_router
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.room import Booking, Room
from app.models.user import User

SEED_ROOMS = [
    ("Sala A", 10, "Mala sala konferencyjna"),
    ("Sala B", 20, "Srednia sala konferencyjna"),
    ("Sala C", 5, "Salka do spotkan"),
    ("Sala Konferencyjna", 30, "Duza sala konferencyjna z rzutnikiem"),
    ("Sala Szkoleniowa", 15, "Sala przystosowana do szkolen"),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        db.add(
            User(
                username="admin",
                email="admin@admin.pl",
                hashed_password=hash_password("Admin123!"),
                role="admin",
            )
        )
        db.commit()
        admin = db.query(User).filter(User.username == "admin").first()

    test_user = db.query(User).filter(User.username == "test").first()
    if not test_user:
        db.add(
            User(
                username="test",
                email="test@test.pl",
                hashed_password=hash_password("Test1234!"),
                role="user",
            )
        )
        db.commit()
        test_user = db.query(User).filter(User.username == "test").first()

    if not db.query(Room).filter(Room.name == SEED_ROOMS[0][0]).first():
        room_objects = []
        for name, capacity, desc in SEED_ROOMS:
            room = Room(name=name, capacity=capacity, description=desc)
            db.add(room)
            db.flush()
            room_objects.append(room)
        db.commit()

        base = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)
        base += timedelta(days=(7 - base.weekday()) % 7)

        sample_bookings = [
            (room_objects[0].id, base, 60, "Spotkanie zespolu"),
            (room_objects[1].id, base + timedelta(days=1), 120, "Warsztaty"),
            (room_objects[3].id, base + timedelta(days=2), 90, "Prezentacja"),
        ]

        for room_id, start, duration_min, title in sample_bookings:
            db.add(
                Booking(
                    room_id=room_id,
                    user_id=test_user.id,
                    start_time=start,
                    end_time=start + timedelta(minutes=duration_min),
                    title=title,
                )
            )
        db.commit()

    db.close()
    yield


app = FastAPI(title="RezerwacjaSal", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(bookings_router)
