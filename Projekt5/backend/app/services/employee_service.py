from functools import reduce
from datetime import date, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employee import Employee, Shift
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, ShiftCreate, ShiftUpdate


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Employee]:
        return self.db.query(Employee).all()

    def get_by_id(self, employee_id: int) -> Employee:
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pracownik nie znaleziony",
            )
        return employee

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(**data.model_dump())
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def update(self, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self.get_by_id(employee_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(employee, key, value)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee_id: int) -> None:
        employee = self.get_by_id(employee_id)
        self.db.delete(employee)
        self.db.commit()

    def add_shift(self, data: ShiftCreate, user_id: int) -> Shift:
        self.get_by_id(data.employee_id)
        shift = Shift(**data.model_dump(), user_id=user_id)
        self.db.add(shift)
        self.db.commit()
        self.db.refresh(shift)
        return shift

    def update_shift(self, shift_id: int, data: ShiftUpdate) -> Shift:
        shift = self.db.query(Shift).filter(Shift.id == shift_id).first()
        if not shift:
            raise HTTPException(status_code=404, detail="Zmiana nie znaleziona")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(shift, key, value)
        self.db.commit()
        self.db.refresh(shift)
        return shift

    def delete_shift(self, shift_id: int) -> None:
        shift = self.db.query(Shift).filter(Shift.id == shift_id).first()
        if not shift:
            raise HTTPException(status_code=404, detail="Zmiana nie znaleziona")
        self.db.delete(shift)
        self.db.commit()


    # ===== ALGORYTM FUNKCYJNY =====

    def get_shifts_for_employee(self, employee_id: int) -> list[Shift]:
        return (
            self.db.query(Shift)
            .filter(Shift.employee_id == employee_id)
            .order_by(Shift.shift_date, Shift.start_time)
            .all()
        )

    def get_weekly_schedule(self, employee_id: int, week_start: date) -> list[dict]:
        self.get_by_id(employee_id)
        week_end = week_start + timedelta(days=7)

        shifts = (
            self.db.query(Shift)
            .filter(
                Shift.employee_id == employee_id,
                Shift.shift_date >= week_start,
                Shift.shift_date < week_end,
            )
            .all()
        )

        result = list(map(
            lambda s: {
                "id": s.id,
                "date": str(s.shift_date),
                "start": str(s.start_time),
                "end": str(s.end_time),
                "task": s.task,
            },
            sorted(shifts, key=lambda s: (s.shift_date, s.start_time)),
        ))
        return result

    def get_total_hours(self, employee_id: int, start: date, end: date) -> float:
        shifts = (
            self.db.query(Shift)
            .filter(
                Shift.employee_id == employee_id,
                Shift.shift_date >= start,
                Shift.shift_date <= end,
            )
            .all()
        )

        total = reduce(
            lambda acc, s: acc + (
                (s.end_time.hour * 60 + s.end_time.minute)
                - (s.start_time.hour * 60 + s.start_time.minute)
            ) / 60,
            shifts,
            0.0,
        )
        return round(total, 2)

    def get_employees_ranking(self, start: date, end: date, limit: int = 10) -> list[dict]:
        employees = self.db.query(Employee).all()

        with_hours = list(map(
            lambda e: {
                "id": e.id,
                "name": e.name,
                "position": e.position,
                "hours": self.get_total_hours(e.id, start, end),
            },
            employees,
        ))

        with_hours = list(filter(lambda e: e["hours"] > 0, with_hours))
        with_hours.sort(key=lambda e: e["hours"], reverse=True)
        return with_hours[:limit]