# Backward compatibility imports
# This file maintains compatibility with existing imports
# New code should use the service layer or specific CRUD modules

import uuid
from typing import Any

from sqlmodel import Session

from app.crud.crud_user import user as user_crud
from app.crud.crud_item import item as item_crud
from app.models import Item, User
from app.schemas import ItemCreate, UserCreate, UserUpdate


# Legacy function names for backward compatibility
def create_user(*, session: Session, user_create: UserCreate) -> User:
    return user_crud.create(session=session, obj_in=user_create)


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    return user_crud.update(session=session, db_obj=db_user, obj_in=user_in)


def get_user_by_email(*, session: Session, email: str) -> User | None:
    return user_crud.get_by_email(session=session, email=email)


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    return user_crud.authenticate(session=session, email=email, password=password)


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    return item_crud.create_with_owner(
        session=session, obj_in=item_in, owner_id=owner_id
    )
