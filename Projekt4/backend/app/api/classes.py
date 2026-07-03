import json
from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.fitness import (
    ClassCreate,
    ClassOut,
    ClassUpdate,
    SignupCreate,
    SignupOut,
    UserClassOut,
    WaitlistEntry,
)
from app.schemas.user import UserOut
from app.services.class_service import FitnessClassService

router = APIRouter(prefix="/api/classes", tags=["classes"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        data = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(data)
            except Exception:
                pass


manager = ConnectionManager()


@router.websocket("/ws")
async def classes_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("", response_model=list[ClassOut])
def get_all(db: Session = Depends(get_db)):
    service = FitnessClassService(db)
    classes = service.get_all()
    return [
        ClassOut(
            id=c.id,
            name=c.name,
            description=c.description,
            instructor=c.instructor,
            datetime=c.datetime,
            capacity=c.capacity,
            created_at=c.created_at,
            free_spots=service.get_free_spots(c.id),
        )
        for c in classes
    ]


@router.get("/available", response_model=list[ClassOut])
def get_available(db: Session = Depends(get_db)):
    service = FitnessClassService(db)
    classes = service.get_available_classes()
    return [
        ClassOut(
            id=c.id,
            name=c.name,
            description=c.description,
            instructor=c.instructor,
            datetime=c.datetime,
            capacity=c.capacity,
            created_at=c.created_at,
            free_spots=service.get_free_spots(c.id),
        )
        for c in classes
    ]


@router.get("/my-classes", response_model=list[UserClassOut])
def get_my_classes(
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FitnessClassService(db)
    classes = service.get_user_classes(current.id)
    return [UserClassOut(**c) for c in classes]


@router.get("/{class_id}", response_model=ClassOut)
def get_by_id(class_id: int, db: Session = Depends(get_db)):
    service = FitnessClassService(db)
    c = service.get_by_id(class_id)
    return ClassOut(
        id=c.id,
        name=c.name,
        description=c.description,
        instructor=c.instructor,
        datetime=c.datetime,
        capacity=c.capacity,
        created_at=c.created_at,
        free_spots=service.get_free_spots(c.id),
    )


@router.post("", response_model=ClassOut, status_code=201)
def create(
    data: ClassCreate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = FitnessClassService(db)
    c = service.create(data)
    return ClassOut(
        id=c.id,
        name=c.name,
        description=c.description,
        instructor=c.instructor,
        datetime=c.datetime,
        capacity=c.capacity,
        created_at=c.created_at,
        free_spots=c.capacity,
    )


@router.patch("/{class_id}", response_model=ClassOut)
def update(
    class_id: int,
    data: ClassUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = FitnessClassService(db)
    c = service.update(class_id, data)
    return ClassOut(
        id=c.id,
        name=c.name,
        description=c.description,
        instructor=c.instructor,
        datetime=c.datetime,
        capacity=c.capacity,
        created_at=c.created_at,
        free_spots=service.get_free_spots(c.id),
    )


@router.delete("/{class_id}", status_code=204)
def delete(
    class_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = FitnessClassService(db)
    service.delete(class_id)


@router.post("/{class_id}/signup", response_model=SignupOut)
async def signup(
    class_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FitnessClassService(db)
    s = service.signup(class_id, current.id)
    await manager.broadcast({
        "event": "new_signup",
        "class_id": class_id,
        "free_spots": service.get_free_spots(class_id),
    })
    return SignupOut.model_validate(s)


@router.delete("/{class_id}/signup", status_code=200)
async def cancel_signup(
    class_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FitnessClassService(db)
    service.cancel_signup(class_id, current.id)
    await manager.broadcast({
        "event": "signup_cancelled",
        "class_id": class_id,
        "free_spots": service.get_free_spots(class_id),
    })
    return {"detail": "Wypisano z zajec"}


@router.get("/{class_id}/waitlist", response_model=list[WaitlistEntry])
def get_waitlist(class_id: int, db: Session = Depends(get_db)):
    service = FitnessClassService(db)
    service.get_by_id(class_id)
    waitlist = service.get_waitlist_for_class(class_id)
    return [
        WaitlistEntry(
            signup_id=s.id,
            user=UserOut.model_validate(s.user),
            signed_up_at=s.signed_up_at,
        )
        for s in waitlist
    ]
