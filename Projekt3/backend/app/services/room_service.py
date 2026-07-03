from datetime import datetime, timedelta
from functools import reduce

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.room import Room, Booking
from app.models.user import User
from app.schemas.room import RoomCreate, RoomUpdate, BookingCreate


class RoomService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Room]:
        return self.db.query(Room).all()

    def get_by_id(self, room_id: int) -> Room:
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala nie znaleziona",
            )
        return room

    def create(self, data: RoomCreate) -> Room:
        room = Room(name=data.name, capacity=data.capacity, description=data.description)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def update(self, room_id: int, data: RoomUpdate) -> Room:
        room = self.get_by_id(room_id)
        if data.name is not None:
            room.name = data.name
        if data.capacity is not None:
            room.capacity = data.capacity
        if data.description is not None:
            room.description = data.description
        self.db.commit()
        self.db.refresh(room)
        return room

    def delete(self, room_id: int) -> None:
        room = self.get_by_id(room_id)
        self.db.delete(room)
        self.db.commit()


class BookingService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user: User) -> list[Booking]:
        if user.role == "admin":
            return self.db.query(Booking).all()
        return self.db.query(Booking).filter(Booking.user_id == user.id).all()

    def create(self, user: User, data: BookingCreate) -> Booking:
        room = self.db.query(Room).filter(Room.id == data.room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala nie znaleziona",
            )
        if data.start_time >= data.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Czas zakonczenia musi byc pozniejszy niz czas rozpoczecia",
            )

        conflicting = (
            self.db.query(Booking)
            .filter(
                Booking.room_id == data.room_id,
                Booking.end_time > data.start_time,
                Booking.start_time < data.end_time,
            )
            .first()
        )
        if conflicting:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sala jest juz zarezerwowana w tym czasie",
            )

        booking = Booking(
            room_id=data.room_id,
            user_id=user.id,
            start_time=data.start_time,
            end_time=data.end_time,
            title=data.title or "",
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def delete(self, booking_id: int, user: User) -> None:
        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rezerwacja nie znaleziona",
            )
        if user.role != "admin" and booking.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nie masz uprawnien do usuniecia tej rezerwacji",
            )
        self.db.delete(booking)
        self.db.commit()

    def get_available_rooms(self, start_time: datetime, end_time: datetime) -> list[Room]:
        all_rooms = self.db.query(Room).all()

        conflicting_bookings = (
            self.db.query(Booking)
            .filter(
                Booking.end_time > start_time,
                Booking.start_time < end_time,
            )
            .all()
        )

        conflicting_room_ids = set(map(lambda b: b.room_id, conflicting_bookings))

        available = list(
            filter(lambda r: r.id not in conflicting_room_ids, all_rooms)
        )

        return available

    def get_conflicts_count(self, room_id: int) -> int:
        bookings = self.db.query(Booking).filter(Booking.room_id == room_id).all()

        def is_conflicting(b1, b2):
            return (
                b1.id != b2.id
                and b1.end_time > b2.start_time
                and b1.start_time < b2.end_time
            )

        pairs = [(b1, b2) for b1 in bookings for b2 in bookings]

        conflicting_pairs = list(filter(lambda p: is_conflicting(p[0], p[1]), pairs))

        count = reduce(lambda acc, _: acc + 1, conflicting_pairs, 0)

        return count // 2

    def get_room_utilization(self) -> list[dict]:
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)

        rooms = self.db.query(Room).all()
        all_bookings = (
            self.db.query(Booking)
            .filter(Booking.start_time >= thirty_days_ago)
            .all()
        )

        total_minutes = 30 * 24 * 60

        def calc_utilization(room):
            room_bookings = list(
                filter(lambda b: b.room_id == room.id, all_bookings)
            )
            used_minutes = reduce(
                lambda acc, b: acc + (b.end_time - b.start_time).total_seconds() / 60,
                room_bookings,
                0.0,
            )
            percentage = (used_minutes / total_minutes) * 100
            return {
                "room_id": room.id,
                "name": room.name,
                "utilization_percent": round(percentage, 2),
            }

        return list(map(calc_utilization, rooms))
