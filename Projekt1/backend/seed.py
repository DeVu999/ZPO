from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.user import User

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

db.close()
