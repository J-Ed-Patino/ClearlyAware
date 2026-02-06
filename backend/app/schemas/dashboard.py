from pydantic import BaseModel


class CategorySummary(BaseModel):
    category_id: str
    category_name: str
    budgeted: float
    spent: float
    percent: int
    remaining: float


class DashboardSummary(BaseModel):
    period: str
    period_type: str
    categories: list[CategorySummary]
    total_budgeted: float
    total_spent: float
    total_percent: int
    total_remaining: float