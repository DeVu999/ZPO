from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("", response_model=list[ItemOut])
def get_all(
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return [ItemOut.model_validate(i) for i in service.get_all(current.id)]


@router.get("/search", response_model=list[ItemOut])
def search(
    keyword: str,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return [ItemOut.model_validate(i) for i in service.search_by_name(current.id, keyword)]


@router.get("/character-count", response_model=int)
def character_count(
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return service.count_characters(current.id)


@router.get("/{item_id}", response_model=ItemOut)
def get_by_id(
    item_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return ItemOut.model_validate(service.get_by_id(item_id, current.id))


@router.post("", response_model=ItemOut, status_code=201)
def create(
    data: ItemCreate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return ItemOut.model_validate(service.create(data, current.id))


@router.patch("/{item_id}", response_model=ItemOut)
def update(
    item_id: int,
    data: ItemUpdate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    return ItemOut.model_validate(service.update(item_id, data, current.id))


@router.delete("/{item_id}", status_code=204)
def delete(
    item_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ItemService(db)
    service.delete(item_id, current.id)


@router.websocket("/ws")
async def items_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
