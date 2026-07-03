from datetime import datetime

from pydantic import BaseModel


class RoomOut(BaseModel):
    id: int
    name: str
    capacity: int
    description: str

    model_config = {"from_attributes": True}


class RoomCreate(BaseModel):
    name: str
    capacity: int
    description: str = ""


class RoomUpdate(BaseModel):
    name: str | None = None
    capacity: int | None = None
    description: str | None = None


class BookingOut(BaseModel):
    id: int
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    title: str | None = None

    model_config = {"from_attributes": True}


class BookingCreate(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    title: str | None = None
