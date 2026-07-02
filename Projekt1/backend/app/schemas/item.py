from datetime import datetime

from pydantic import BaseModel


class ItemOut(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    owner_id: int

    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    name: str
    description: str = ""


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
