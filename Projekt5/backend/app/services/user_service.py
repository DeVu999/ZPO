from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Użytkownik nie znaleziony",
            )
        return user

    def update_role(self, user_id: int, role: str) -> User:
        if role not in ("admin", "user"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nieprawidłowa rola",
            )
        user = self.get_by_id(user_id)
        user.role = role
        self.db.commit()
        self.db.refresh(user)
        return user

    def toggle_active(self, user_id: int) -> User:
        user = self.get_by_id(user_id)
        user.is_active = not user.is_active
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.db.delete(user)
        self.db.commit()
