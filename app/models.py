# Backward compatibility imports
# This file maintains compatibility with existing imports
# New code should import from the specific modules

from app.models.user import User
from app.models.item import Item
from app.schemas import (
    # User schemas
    UserBase,
    UserCreate,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
    UpdatePassword,
    UserPublic,
    UsersPublic,
    # Item schemas
    ItemBase,
    ItemCreate,
    ItemUpdate,
    ItemPublic,
    ItemsPublic,
    # Common schemas
    Message,
    # Auth schemas
    Token,
    TokenPayload,
    NewPassword,
)

# Keep all imports for backward compatibility
__all__ = [
    # Models
    "User",
    "Item",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserRegister",
    "UserUpdate",
    "UserUpdateMe",
    "UpdatePassword",
    "UserPublic",
    "UsersPublic",
    # Item schemas
    "ItemBase",
    "ItemCreate",
    "ItemUpdate",
    "ItemPublic",
    "ItemsPublic",
    # Common schemas
    "Message",
    # Auth schemas
    "Token",
    "TokenPayload",
    "NewPassword",
]
