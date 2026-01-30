from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from app.services.budget import create_budget, get_budgets, get_budget_by_id, update_budget, delete_budget

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create(budget_date: BudgetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget = create_budget(db, current_user.id, budget_date)
    return budget


@router.get("", response_model=list[BudgetResponse])
def list_budgets(period_type: str = None, start_date: date = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_budgets(db, current_user.id, period_type, start_date)


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_single_budget(budget_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget = get_budget_by_id(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
def update(budget_id: UUID, budget_data: BudgetUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget = get_budget_by_id(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return update_budget(db, budget, budget_data)


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(budget_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget = get_budget_by_id(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    delete_budget(db, budget)