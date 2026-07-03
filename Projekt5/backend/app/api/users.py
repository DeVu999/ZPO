from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.user import UserOut, UserRoleUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def get_all(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    service = UserService(db)
    return [UserOut.model_validate(u) for u in service.get_all()]


@router.get("/{user_id}", response_model=UserOut)
def get_by_id(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return UserOut.model_validate(service.get_by_id(user_id))


@router.patch("/{user_id}/role", response_model=UserOut)
def update_role(
    user_id: int,
    data: UserRoleUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return UserOut.model_validate(service.update_role(user_id, data.role))


@router.patch("/{user_id}/toggle-active", response_model=UserOut)
def toggle_active(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return UserOut.model_validate(service.toggle_active(user_id))


@router.delete("/{user_id}", status_code=204)
def delete(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    service.delete(user_id)
