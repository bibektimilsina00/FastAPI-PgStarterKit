import uuid
from typing import Any

from sqlmodel import Session

from app import crud
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    @staticmethod
    def create_user(*, session: Session, user_create: UserCreate) -> User:
        return crud.user.create(session=session, obj_in=user_create)

    @staticmethod
    def get_user(session: Session, user_id: uuid.UUID) -> User | None:
        return crud.user.get(session=session, id=user_id)

    @staticmethod
    def get_user_by_email(*, session: Session, email: str) -> User | None:
        return crud.user.get_by_email(session=session, email=email)

    @staticmethod
    def get_users(session: Session, *, skip: int = 0, limit: int = 100) -> list[User]:
        return crud.user.get_multi(session=session, skip=skip, limit=limit)

    @staticmethod
    def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> User:
        return crud.user.update(session=session, db_obj=db_user, obj_in=user_in)

    @staticmethod
    def authenticate_user(
        *, session: Session, email: str, password: str
    ) -> User | None:
        return crud.user.authenticate(session=session, email=email, password=password)

    @staticmethod
    def is_active(user: User) -> bool:
        return crud.user.is_active(user)

    @staticmethod
    def is_superuser(user: User) -> bool:
        return crud.user.is_superuser(user)

    @staticmethod
    def count_users(session: Session) -> int:
        return crud.user.count(session=session)


user_service = UserService()
