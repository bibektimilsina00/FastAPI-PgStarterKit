import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.schemas.item import ItemBase

if TYPE_CHECKING:
    from app.models.user import User


class Item(ItemBase, table=True):
    """Item database model"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User | None" = Relationship(back_populates="items")
