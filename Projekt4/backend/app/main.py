from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, classes, users
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.fitness import FitnessClass, Signup
from app.models.user import User

SEED_CLASSES = [
    {
        "name": "Joga poranna",
        "description": "Relaksujace zajecia jogi na dobry poczatek dnia.",
        "instructor": "Anna Kowalska",
        "hours": 24,
        "capacity": 20,
    },
    {
        "name": "CrossFit",
        "description": "Intensywny trening funkcjonalny dla zaawansowanych.",
        "instructor": "Jan Nowak",
        "hours": 48,
        "capacity": 15,
    },
    {
        "name": "Zumba",
        "description": "Energetyczne zajecia taneczne przy latynoskiej muzyce.",
        "instructor": "Maria Wisniewska",
        "hours": 72,
        "capacity": 25,
    },
    {
        "name": "Pilates",
        "description": "Wzmacnianie miesni glebokich i poprawa postawy ciala.",
        "instructor": "Katarzyna Zielinska",
        "hours": 96,
        "capacity": 2,
    },
    {
        "name": "Cardio",
        "description": "Trening wydolnosciowy spalajacy kalorie.",
        "instructor": "Piotr Lewandowski",
        "hours": 120,
        "capacity": 30,
    },
    {
        "name": "Stretching",
        "description": "Rozciaganie i poprawa elastycznosci calego ciala.",
        "instructor": "Agnieszka Kaminska",
        "hours": 168,
        "capacity": 12,
    },
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

    user2 = db.query(User).filter(User.username == "user2").first()
    if not user2:
        db.add(
            User(
                username="user2",
                email="user2@test.pl",
                hashed_password=hash_password("Test1234!"),
                role="user",
            )
        )
        db.commit()
        user2 = db.query(User).filter(User.username == "user2").first()

    if not db.query(FitnessClass).filter(FitnessClass.name == SEED_CLASSES[0]["name"]).first():
        now = datetime.now(timezone.utc)
        for data in SEED_CLASSES:
            c = FitnessClass(
                name=data["name"],
                description=data["description"],
                instructor=data["instructor"],
                datetime=now + timedelta(hours=data["hours"]),
                capacity=data["capacity"],
            )
            db.add(c)
        db.commit()

        all_classes = db.query(FitnessClass).all()
        pilates = next(c for c in all_classes if c.name == "Pilates")

        db.add(Signup(class_id=pilates.id, user_id=test_user.id, is_waitlisted=False))
        db.add(Signup(class_id=pilates.id, user_id=user2.id, is_waitlisted=False))
        db.add(Signup(class_id=pilates.id, user_id=admin.id, is_waitlisted=True))
        db.commit()

        joga = next(c for c in all_classes if c.name == "Joga poranna")
        db.add(Signup(class_id=joga.id, user_id=test_user.id, is_waitlisted=False))
        db.commit()

        crossfit = next(c for c in all_classes if c.name == "CrossFit")
        db.add(Signup(class_id=crossfit.id, user_id=test_user.id, is_waitlisted=False))
        db.add(Signup(class_id=crossfit.id, user_id=user2.id, is_waitlisted=False))
        db.commit()

        zumba = next(c for c in all_classes if c.name == "Zumba")
        db.add(Signup(class_id=zumba.id, user_id=admin.id, is_waitlisted=False))
        db.commit()

        cardio = next(c for c in all_classes if c.name == "Cardio")
        db.add(Signup(class_id=cardio.id, user_id=test_user.id, is_waitlisted=False))
        db.add(Signup(class_id=cardio.id, user_id=user2.id, is_waitlisted=False))
        db.commit()

    db.close()
    yield


app = FastAPI(title="ZapisyFitness", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classes.router)
