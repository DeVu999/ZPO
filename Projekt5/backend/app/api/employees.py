from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeOut,
    EmployeeUpdate,
    ShiftCreate,
    ShiftOut,
    ShiftUpdate,
)
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/api/employees", tags=["employees"])



@router.get("", response_model=list[EmployeeOut])
def get_all(db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return [EmployeeOut.model_validate(e) for e in service.get_all()]


@router.get("/ranking")
def get_ranking(
    start_date: str,
    end_date: str,
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
):
    from datetime import date
    service = EmployeeService(db)
    return service.get_employees_ranking(
        date.fromisoformat(start_date), date.fromisoformat(end_date), limit
    )


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_by_id(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return EmployeeOut.model_validate(service.get_by_id(employee_id))


@router.post("", response_model=EmployeeOut, status_code=201)
def create(
    data: EmployeeCreate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return EmployeeOut.model_validate(service.create(data))


@router.patch("/{employee_id}", response_model=EmployeeOut)
def update(
    employee_id: int,
    data: EmployeeUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return EmployeeOut.model_validate(service.update(employee_id, data))


@router.delete("/{employee_id}", status_code=204)
def delete(
    employee_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    service.delete(employee_id)




@router.get("/{employee_id}/shifts", response_model=list[ShiftOut])
def get_shifts(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return [ShiftOut.model_validate(s) for s in service.get_shifts_for_employee(employee_id)]


@router.get("/{employee_id}/weekly-schedule")
def weekly_schedule(employee_id: int, week_start: str, db: Session = Depends(get_db)):
    from datetime import date
    service = EmployeeService(db)
    return service.get_weekly_schedule(employee_id, date.fromisoformat(week_start))


@router.get("/{employee_id}/total-hours")
def total_hours(employee_id: int, start_date: str, end_date: str, db: Session = Depends(get_db)):
    from datetime import date
    service = EmployeeService(db)
    return service.get_total_hours(
        employee_id, date.fromisoformat(start_date), date.fromisoformat(end_date)
    )


@router.post("/shifts", response_model=ShiftOut, status_code=201)
def create_shift(
    data: ShiftCreate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return ShiftOut.model_validate(service.add_shift(data, current.id))


@router.patch("/shifts/{shift_id}", response_model=ShiftOut)
def update_shift(
    shift_id: int,
    data: ShiftUpdate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    return ShiftOut.model_validate(service.update_shift(shift_id, data))


@router.delete("/shifts/{shift_id}", status_code=204)
def delete_shift(
    shift_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = EmployeeService(db)
    service.delete_shift(shift_id)


@router.websocket("/ws")
async def employees_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Grafik zaktualizowany: {data}")
    except WebSocketDisconnect:
        pass