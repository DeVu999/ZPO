from functools import reduce

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.items import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int) -> list[Item]:
        return self.db.query(Item).filter(Item.owner_id == user_id).all()

    def get_by_id(self, item_id: int, user_id: int) -> Item:
        item = (
            self.db.query(Item)
            .filter(Item.id == item_id, Item.owner_id == user_id)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Przedmiot nie znaleziony",
            )
        return item

    def create(self, data: ItemCreate, user_id: int) -> Item:
        item = Item(**data.model_dump(), owner_id=user_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item_id: int, data: ItemUpdate, user_id: int) -> Item:
        item = self.get_by_id(item_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int, user_id: int) -> None:
        item = self.get_by_id(item_id, user_id)
        self.db.delete(item)
        self.db.commit()

    def search_by_name(self, user_id: int, keyword: str) -> list[Item]:
        items = self.get_all(user_id)
        return list(
            filter(lambda i: keyword.lower() in i.name.lower(), items)
        )

    def count_characters(self, user_id: int) -> int:
        items = self.get_all(user_id)
        return reduce(lambda acc, i: acc + len(i.description), items, 0)
