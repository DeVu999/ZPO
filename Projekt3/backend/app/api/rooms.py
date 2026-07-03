from datetime import datetime

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.room import (
    BookingCreate,
    BookingOut,
    RoomCreate,
    RoomOut,
    RoomUpdate,
)
from app.services.room_service import BookingService, RoomService

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

bookings_router = APIRouter(prefix="/api/bookings", tags=["bookings"])

active_connections: list[WebSocket] = []


async def broadcast(message: dict):
    for ws in active_connections:
        try:
            await ws.send_json(message)
        except Exception:
            active_connections.remove(ws)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.get("", response_model=list[RoomOut])
def get_all_rooms(db: Session = Depends(get_db)):
    service = RoomService(db)
    return [RoomOut.model_validate(r) for r in service.get_all()]


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return RoomOut.model_validate(service.get_by_id(room_id))


@router.post("", response_model=RoomOut)
def create_room(
    data: RoomCreate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = RoomService(db)
    return RoomOut.model_validate(service.create(data))


@router.patch("/{room_id}", response_model=RoomOut)
def update_room(
    room_id: int,
    data: RoomUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = RoomService(db)
    return RoomOut.model_validate(service.update(room_id, data))


@router.delete("/{room_id}", status_code=204)
def delete_room(
    room_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = RoomService(db)
    service.delete(room_id)


@router.get("/{room_id}/conflicts", response_model=dict)
def get_room_conflicts(
    room_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = BookingService(db)
    count = service.get_conflicts_count(room_id)
    return {"room_id": room_id, "conflicts": count}


@router.get("/stats/utilization", response_model=list[dict])
def get_utilization(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = BookingService(db)
    return service.get_room_utilization()


@bookings_router.get("/available", response_model=list[RoomOut])
def get_available_rooms(
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    db: Session = Depends(get_db),
):
    service = BookingService(db)
    rooms = service.get_available_rooms(start_time, end_time)
    return [RoomOut.model_validate(r) for r in rooms]


@bookings_router.get("", response_model=list[BookingOut])
def get_all_bookings(
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)
    return [BookingOut.model_validate(b) for b in service.get_all(current)]


@bookings_router.post("", response_model=BookingOut)
async def create_booking(
    data: BookingCreate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)
    booking = service.create(current, data)
    await broadcast(
        {
            "event": "booking_created",
            "booking": BookingOut.model_validate(booking).model_dump(mode="json"),
        }
    )
    return BookingOut.model_validate(booking)


@bookings_router.delete("/{booking_id}", status_code=204)
async def delete_booking(
    booking_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)
    service.delete(booking_id, current)
    await broadcast({"event": "booking_deleted", "booking_id": booking_id})
