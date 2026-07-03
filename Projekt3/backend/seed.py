from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.user import User
from app.models.room import Room, Booking
from datetime import datetime, timedelta

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
    test_user = User(
        username="test",
        email="test@test.pl",
        hashed_password=hash_password("Test1234!"),
        role="user",
    )
    db.add(test_user)
    db.commit()
    print("Utworzono konto testowe: test / Test1234!")
else:
    print("Konto testowe juz istnieje")

rooms_data = [
    ("Sala A", 10, "Mala sala konferencyjna"),
    ("Sala B", 20, "Srednia sala konferencyjna"),
    ("Sala C", 5, "Salka do spotkan"),
    ("Sala Konferencyjna", 30, "Duza sala konferencyjna z rzutnikiem"),
    ("Sala Szkoleniowa", 15, "Sala przystosowana do szkolen"),
]

room_objects = []
for name, capacity, desc in rooms_data:
    existing_room = db.query(Room).filter(Room.name == name).first()
    if not existing_room:
        room = Room(name=name, capacity=capacity, description=desc)
        db.add(room)
        db.flush()
        room_objects.append(room)
        print(f"Dodano sale: {name}")
    else:
        room_objects.append(existing_room)

db.commit()

if test_user and room_objects:
    existing_booking = db.query(Booking).first()
    if not existing_booking:
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
        print("Dodano 3 przykladowe rezerwacje")

db.close()
print("Seed zakonczony")
