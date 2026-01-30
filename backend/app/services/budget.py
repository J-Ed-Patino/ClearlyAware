from datetime import date
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate

def create_budget(db: Session, user_id: UUID, budget_data: BudgetCreate) -> Budget:
    budget = Budget(
        user_id=user_id,
        category_id=budget_data.category_id,
        amount=budget_data.amount,
        period_type=budget_data.period_type,
        start_date=budget_data.start_date,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budgets(db: Session, user_id: UUID, period_type: str = None, start_date: date = None) -> Budget | None:
    query = db.query(Budget).filter(Budget.user_id == user_id)
    if period_type:
        query = query.filter(Budget.period_type == period_type)
    if start_date:
        query = query.filter(Budget.period_type == period_type)
    return query.all()


def get_budget_by_id(db: Session, budget_id: UUID, user_id: UUID) -> Budget | None:
    return db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).first()


def update_budget(db: Session, budget: Budget, budget_data_update: BudgetUpdate) -> Budget:
    budget.amount = budget_data_update.amount
    db.commit()
    db.refresh(budget)
    return budget

def delete_budget(db: Session, budget: Budget) -> None:
    db.delete(budget)
    db.commit()