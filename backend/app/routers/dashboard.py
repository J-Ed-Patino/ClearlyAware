from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def summary( period_type: str = "monthly", start_date: date = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_dashboard_summary(db, current_user.id, period_type, start_date)