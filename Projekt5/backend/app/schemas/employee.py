from datetime import date, time, datetime

from pydantic import BaseModel


class EmployeeOut(BaseModel):
    id: int
    name: str
    position: str
    department: str
    created_at: datetime

    model_config = {"from_attributes": True}


class EmployeeCreate(BaseModel):
    name: str
    position: str
    department: str = ""


class EmployeeUpdate(BaseModel):
    name: str | None = None
    position: str | None = None
    department: str | None = None


class ShiftOut(BaseModel):
    id: int
    employee_id: int
    user_id: int
    shift_date: date
    start_time: time
    end_time: time
    task: str

    model_config = {"from_attributes": True}


class ShiftCreate(BaseModel):
    employee_id: int
    shift_date: date
    start_time: time
    end_time: time
    task: str = ""


class ShiftUpdate(BaseModel):
    shift_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    task: str | None = None