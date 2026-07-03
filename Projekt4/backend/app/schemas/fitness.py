from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserOut


class ClassOut(BaseModel):
    id: int
    name: str
    description: str
    instructor: str
    datetime: datetime
    capacity: int
    created_at: datetime
    free_spots: int = 0

    model_config = {"from_attributes": True}


class ClassCreate(BaseModel):
    name: str
    description: str = ""
    instructor: str
    datetime: datetime
    capacity: int


class ClassUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None
    datetime: Optional[datetime] = None
    capacity: Optional[int] = None


class SignupOut(BaseModel):
    id: int
    class_id: int
    user_id: int
    is_waitlisted: bool
    signed_up_at: datetime

    model_config = {"from_attributes": True}


class SignupCreate(BaseModel):
    pass


class WaitlistEntry(BaseModel):
    signup_id: int
    user: UserOut
    signed_up_at: datetime

    model_config = {"from_attributes": True}


class UserClassOut(BaseModel):
    signup_id: int
    class_name: str
    instructor: str
    datetime: datetime
    is_waitlisted: bool
    signed_up_at: datetime
