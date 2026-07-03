from datetime import datetime, timedelta, timezone

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.user import User
from app.models.fitness import FitnessClass, Signup

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
    print("Utworzono konto: test / Test1234!")

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
    print("Utworzono konto: user2 / Test1234!")

classes_data = [
    ("Joga poranna", "Relaksujace zajecia jogi na dobry poczatek dnia.", "Anna Kowalska", 24, 20),
    ("CrossFit", "Intensywny trening funkcjonalny dla zaawansowanych.", "Jan Nowak", 48, 15),
    ("Zumba", "Energetyczne zajecia taneczne przy latynoskiej muzyce.", "Maria Wisniewska", 72, 25),
    ("Pilates", "Wzmacnianie miesni glebokich i poprawa postawy ciala.", "Katarzyna Zielinska", 96, 2),
    ("Cardio", "Trening wydolnosciowy spalajacy kalorie.", "Piotr Lewandowski", 120, 30),
    ("Stretching", "Rozciaganie i poprawa elastycznosci calego ciala.", "Agnieszka Kaminska", 168, 12),
]

now = datetime.now(timezone.utc)
added = 0
for name, desc, instructor, hours, capacity in classes_data:
    if not db.query(FitnessClass).filter(FitnessClass.name == name).first():
        db.add(
            FitnessClass(
                name=name,
                description=desc,
                instructor=instructor,
                datetime=now + timedelta(hours=hours),
                capacity=capacity,
            )
        )
        added += 1

db.commit()
print(f"Dodano {added} zajec fitness")

if not db.query(Signup).first():
    all_classes = db.query(FitnessClass).all()
    users = db.query(User).all()
    test_u = db.query(User).filter(User.username == "test").first()
    user2_u = db.query(User).filter(User.username == "user2").first()
    admin_u = db.query(User).filter(User.username == "admin").first()

    pilates = next(c for c in all_classes if c.name == "Pilates")
    db.add(Signup(class_id=pilates.id, user_id=test_u.id, is_waitlisted=False))
    db.add(Signup(class_id=pilates.id, user_id=user2_u.id, is_waitlisted=False))
    db.add(Signup(class_id=pilates.id, user_id=admin_u.id, is_waitlisted=True))

    joga = next(c for c in all_classes if c.name == "Joga poranna")
    db.add(Signup(class_id=joga.id, user_id=test_u.id, is_waitlisted=False))

    crossfit = next(c for c in all_classes if c.name == "CrossFit")
    db.add(Signup(class_id=crossfit.id, user_id=test_u.id, is_waitlisted=False))
    db.add(Signup(class_id=crossfit.id, user_id=user2_u.id, is_waitlisted=False))

    zumba = next(c for c in all_classes if c.name == "Zumba")
    db.add(Signup(class_id=zumba.id, user_id=admin_u.id, is_waitlisted=False))

    cardio = next(c for c in all_classes if c.name == "Cardio")
    db.add(Signup(class_id=cardio.id, user_id=test_u.id, is_waitlisted=False))
    db.add(Signup(class_id=cardio.id, user_id=user2_u.id, is_waitlisted=False))

    db.commit()
    print("Dodano przykladowe zapisy")

db.close()
