from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    # Lets Pydantic read from SQLAlchemy model objects, not just dicts.
    class Config:
        from_attributes = True