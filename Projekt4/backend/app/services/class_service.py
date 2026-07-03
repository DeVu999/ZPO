from functools import reduce

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.fitness import FitnessClass, Signup
from app.models.user import User
from app.schemas.fitness import ClassCreate, ClassUpdate


class FitnessClassService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[FitnessClass]:
        return self.db.query(FitnessClass).all()

    def get_by_id(self, class_id: int) -> FitnessClass:
        c = self.db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Zajecia nie znalezione",
            )
        return c

    def create(self, data: ClassCreate) -> FitnessClass:
        c = FitnessClass(**data.model_dump())
        self.db.add(c)
        self.db.commit()
        self.db.refresh(c)
        return c

    def update(self, class_id: int, data: ClassUpdate) -> FitnessClass:
        c = self.get_by_id(class_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(c, key, value)
        self.db.commit()
        self.db.refresh(c)
        return c

    def delete(self, class_id: int) -> None:
        c = self.get_by_id(class_id)
        self.db.delete(c)
        self.db.commit()

    def get_free_spots(self, class_id: int) -> int:
        c = self.db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
        if not c:
            return 0
        count = self.db.query(Signup).filter(
            Signup.class_id == class_id, Signup.is_waitlisted == False
        ).count()
        return max(0, c.capacity - count)

    def get_available_classes(self) -> list[FitnessClass]:
        classes = self.db.query(FitnessClass).all()
        all_confirmed = self.db.query(Signup).filter(
            Signup.is_waitlisted == False
        ).all()

        counts = dict(
            reduce(
                lambda acc, s: {**acc, s.class_id: acc.get(s.class_id, 0) + 1},
                all_confirmed,
                {},
            )
        )

        available = list(
            filter(
                lambda c: counts.get(c.id, 0) < c.capacity,
                classes,
            )
        )
        return available

    def get_waitlist_for_class(self, class_id: int) -> list[Signup]:
        signups = self.db.query(Signup).filter(
            Signup.class_id == class_id, Signup.is_waitlisted == True
        ).all()
        return sorted(signups, key=lambda s: s.signed_up_at)

    def promote_from_waitlist(self, class_id: int) -> Signup | None:
        waitlist = self.get_waitlist_for_class(class_id)
        if not waitlist:
            return None
        oldest = waitlist[0]
        oldest.is_waitlisted = False
        self.db.commit()
        self.db.refresh(oldest)
        return oldest

    def get_user_signups(self, user_id: int) -> list[Signup]:
        signups = self.db.query(Signup).filter(Signup.user_id == user_id).all()
        return signups

    def get_user_classes(self, user_id: int) -> list[dict]:
        signups = self.get_user_signups(user_id)
        result = list(
            map(
                lambda s: {
                    "signup_id": s.id,
                    "class_name": s.fitness_class.name,
                    "instructor": s.fitness_class.instructor,
                    "datetime": s.fitness_class.datetime,
                    "is_waitlisted": s.is_waitlisted,
                    "signed_up_at": s.signed_up_at,
                },
                signups,
            )
        )
        return result

    def signup(self, class_id: int, user_id: int) -> Signup:
        c = self.get_by_id(class_id)

        existing = self.db.query(Signup).filter(
            Signup.class_id == class_id, Signup.user_id == user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Juz jestes zapisany na te zajecia",
            )

        confirmed_count = self.db.query(Signup).filter(
            Signup.class_id == class_id, Signup.is_waitlisted == False
        ).count()

        is_waitlisted = confirmed_count >= c.capacity

        signup = Signup(
            class_id=class_id,
            user_id=user_id,
            is_waitlisted=is_waitlisted,
        )
        self.db.add(signup)
        self.db.commit()
        self.db.refresh(signup)
        return signup

    def cancel_signup(self, class_id: int, user_id: int) -> None:
        signup = self.db.query(Signup).filter(
            Signup.class_id == class_id, Signup.user_id == user_id
        ).first()
        if not signup:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nie znaleziono zapisu",
            )

        was_confirmed = not signup.is_waitlisted
        self.db.delete(signup)
        self.db.commit()

        if was_confirmed:
            self.promote_from_waitlist(class_id)
