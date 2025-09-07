import uuid
from typing import Any

from sqlmodel import Session

from app import crud
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    @staticmethod
    def create_item(
        *, session: Session, item_in: ItemCreate, owner_id: uuid.UUID
    ) -> Item:
        return crud.item.create_with_owner(
            session=session, obj_in=item_in, owner_id=owner_id
        )

    @staticmethod
    def get_item(session: Session, item_id: uuid.UUID) -> Item | None:
        return crud.item.get(session=session, id=item_id)

    @staticmethod
    def get_items(session: Session, *, skip: int = 0, limit: int = 100) -> list[Item]:
        return crud.item.get_multi(session=session, skip=skip, limit=limit)

    @staticmethod
    def get_items_by_owner(
        session: Session,
        *,
        owner_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Item]:
        return crud.item.get_multi_by_owner(
            session=session, owner_id=owner_id, skip=skip, limit=limit
        )

    @staticmethod
    def update_item(*, session: Session, db_item: Item, item_in: ItemUpdate) -> Item:
        return crud.item.update(session=session, db_obj=db_item, obj_in=item_in)

    @staticmethod
    def delete_item(*, session: Session, item_id: uuid.UUID) -> Item:
        return crud.item.remove(session=session, id=item_id)

    @staticmethod
    def count_items(session: Session) -> int:
        return crud.item.count(session=session)

    @staticmethod
    def count_items_by_owner(session: Session, *, owner_id: uuid.UUID) -> int:
        return crud.item.count_by_owner(session=session, owner_id=owner_id)


item_service = ItemService()
