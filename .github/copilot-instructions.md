# Copilot Instructions for FastAPI-PgStarterKit

## Architecture Overview

This is a modern FastAPI backend with **clean architecture** using **domain-driven design**:

```
app/
├── models/           # SQLModel database models (inherit from schema bases)
├── schemas/          # Pydantic schemas for API/validation
├── crud/            # Type-safe database operations
├── services/        # Business logic layer
├── api/routes/      # FastAPI route handlers
└── core/           # Configuration, database, security
```

**Key Pattern**: Models extend schema bases (`User(UserBase, table=True)`) to ensure schema-model consistency.

## Development Commands

Use `uv` package manager for all Python operations:

- **Run app**: `uv run uvicorn app.main:app --reload`
- **Tests**: `uv run ./scripts/test.sh` or `uv run pytest`
- **DB migrations**: `uv run alembic upgrade head`
- **Install deps**: `uv add <package>` or `uv add --group dev <package>`

## Essential Patterns

### 1. Model-Schema Pattern

```python
# schemas/user.py - Base properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True

# models/user.py - Database model inherits from base
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
```

### 2. Layered Service Architecture

**Route → Service → CRUD → Model** (never skip layers)

```python
# Route calls service
users = user_service.get_users(session, skip=skip, limit=limit)
# Service calls CRUD
return crud.user.get_multi(session=session, skip=skip, limit=limit)
# CRUD handles database operations
```

### 3. Type Conversion at Route Level

Models ≠ Public schemas. Always convert in routes:

```python
users = user_service.get_users(session, skip=skip, limit=limit)
users_public = [UserPublic.model_validate(user) for user in users]
return UsersPublic(data=users_public, count=count)
```

### 4. Circular Import Prevention

Use `TYPE_CHECKING` for model relationships:

```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.item import Item

class User(UserBase, table=True):
    items: list["Item"] = Relationship(back_populates="owner")
```

## Security & Authentication

- **JWT tokens** with `app.core.security`
- **Password hashing** with bcrypt in CRUD layer
- **Dependencies**: `CurrentUser`, `SessionDep`, `get_current_active_superuser`
- **Superuser creation** handled in `app.core.db.init_db()`

## Database Patterns

- **SQLModel** for both Pydantic schemas and SQLAlchemy tables
- **UUID primary keys** with `uuid.uuid4` default factory
- **Alembic migrations** in `app/alembic/`
- **Relationships** use `cascade_delete=True` for proper cleanup
- **Session dependency** injection via `SessionDep`

## Import Conventions

```python
# Specific imports (preferred)
from app.models.user import User
from app.schemas.user import UserCreate, UserPublic
from app.services import user_service
from app.crud import user

# Avoid generic imports like:
from app.models import *  # Don't do this
```

## Testing & Quality

- **Pytest** with coverage reporting
- **Type checking** with mypy
- **Linting** with ruff
- **Test utilities** in `app/tests/utils/`

## Critical Files

- `app/crud/base.py` - Generic CRUD base class with type safety
- `app/api/deps.py` - Dependency injection setup
- `app/core/config.py` - Environment-based configuration
- `app/main.py` - FastAPI app initialization with CORS/middleware

When adding new features, follow the established domain pattern: create corresponding files in models/, schemas/, crud/, services/, and api/routes/.
