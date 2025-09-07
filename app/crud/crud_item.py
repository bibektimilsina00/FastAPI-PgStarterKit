import uuid
from typing import Any

from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, session: Session, *, obj_in: ItemCreate, owner_id: uuid.UUID
    ) -> Item:
        obj_in_data = obj_in.model_dump()
        db_obj = Item(**obj_in_data, owner_id=owner_id)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self,
        session: Session,
        *,
        owner_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Item]:
        statement = (
            select(Item).where(Item.owner_id == owner_id).offset(skip).limit(limit)
        )
        return list(session.exec(statement).all())

    def count_by_owner(self, session: Session, *, owner_id: uuid.UUID) -> int:
        from sqlmodel import func

        statement = (
            select(func.count()).select_from(Item).where(Item.owner_id == owner_id)
        )
        return session.exec(statement).one()


item = CRUDItem(Item)
