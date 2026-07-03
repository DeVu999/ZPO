from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, movies, users
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.movie import Movie, Rating
from app.models.user import User

SEED_MOVIES = [
    ("Skazani na Shawshank", "Dramat więzienny o nadziei i przyjaźni.", "Dramat"),
    ("Pulp Fiction", "Kultowy film Quentina Tarantino.", "Akcja"),
    ("Incepcja", "Złodziej wkracza w sny innych ludzi.", "Sci-Fi"),
    ("Milczenie owiec", "Agentka FBI szuka pomocy u seryjnego mordercy.", "Thriller"),
    ("Nietykalni", "Opiekun pomaga sparaliżowanemu milionerowi.", "Komedia"),
    ("Obcy - ósmy pasażer Nostromo", "Kosmiczny horror Ridleya Scotta.", "Horror"),
    ("Forrest Gump", "Niezwykła historia prostego człowieka.", "Dramat"),
    ("Leon Zawodowiec", "Płatny zabójca opiekuje się dziewczynką.", "Akcja"),
    ("Matrix", "Haker odkrywa prawdę o rzeczywistości.", "Sci-Fi"),
    ("Siedem", "Dwóch detektywów tropi seryjnego mordercę.", "Thriller"),
]

SAMPLE_RATINGS = [5, 4, 5, 4, 4, 3, 5, 4, 5, 4]


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

    if not db.query(Movie).filter(Movie.title == SEED_MOVIES[0][0]).first():
        for i, (title, desc, genre) in enumerate(SEED_MOVIES):
            movie = Movie(title=title, description=desc, genre=genre)
            db.add(movie)
            db.flush()
            db.add(
                Rating(
                    movie_id=movie.id,
                    user_id=test_user.id,
                    score=SAMPLE_RATINGS[i],
                )
            )
        db.commit()

    db.close()
    yield


app = FastAPI(title="OcenaFilmow", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(movies.router)
