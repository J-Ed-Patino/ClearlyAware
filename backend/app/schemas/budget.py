from datetime import date, datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

VALID_PERIOD_TYPES = Literal["monthly", "weekly", "yearly"]


class BudgetCreate(BaseModel):
    category_id: UUID
    amount: float = Field(gt=0)
    period_type: VALID_PERIOD_TYPES = "monthly"
    start_date: date


class BudgetUpdate(BaseModel):
    amount: float = Field(gt=0)


class BudgetResponse(BaseModel):
    id : UUID
    user_id: UUID
    category_id: UUID
    amount: float
    period_type: str
    start_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

