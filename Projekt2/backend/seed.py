from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.user import User
from app.models.movie import Movie

Base.metadata.create_all(bind=engine)
db = SessionLocal()

existing = db.query(User).filter(User.username == "admin").first()
if existing:
    existing.role = "admin"
    db.commit()
    print("Admin juz istnial - rola ustawiona na 'admin'")
else:
    admin = User(
        username="admin",
        email="admin@admin.pl",
        hashed_password=hash_password("Admin123!"),
        role="admin",
    )
    db.add(admin)
    db.commit()
    print("Utworzono konto admina: admin / Admin123!")

movies = [
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

for title, desc, genre in movies:
    if not db.query(Movie).filter(Movie.title == title).first():
        db.add(Movie(title=title, description=desc, genre=genre))

db.commit()
print(f"Dodano {len(movies)} filmów")

db.close()
