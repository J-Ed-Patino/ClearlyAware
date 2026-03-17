from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.dashboard import DashboardSummary, CategorySummary


def get_period_end_date(start_date: date, period_type: str) -> date:
    if period_type == "weekly":
        return start_date + timedelta(days=7)
    elif period_type == "yearly":
        return start_date.replace(year=start_date.year + 1)
    else:  # monthly
        if start_date.month == 12:
            return start_date.replace(year=start_date.year + 1, month=1)
        return start_date.replace(month=start_date.month + 1)


def get_dashboard_summary(db: Session, user_id: UUID, period_type: str = "monthly", start_date: date = None) -> DashboardSummary:
    if not start_date:
        today = date.today()
        start_date = date(today.year, today.month, 1)

    end_date = get_period_end_date(start_date, period_type)

    # Sum real transactions by category for the period, excluding pending
    spent_by_category = dict(
        db.query(Transaction.category_name, func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date < end_date,
            Transaction.pending == False,
        )
        .group_by(Transaction.category_name)
        .all()
    )

    results = (
        db.query(Category, Budget)
        .outerjoin(
            Budget,
            (Budget.category_id == Category.id)
            & (Budget.user_id == user_id)
            & (Budget.period_type == period_type)
            & (Budget.start_date == start_date),
        )
        .all()
    )

    categories_summary = []
    total_budgeted = 0.0
    total_spent = 0.0

    for category, budget in results:
        category_name = category.name
        spent = float(spent_by_category.get(category_name, 0.0))
        budgeted = float(budget.amount) if budget else 0.0

        percent = int((spent / budgeted * 100)) if budgeted > 0 else 0
        remaining = budgeted - spent

        categories_summary.append(CategorySummary(
            category_id=str(category.id),
            category_name=category_name,
            budgeted=budgeted,
            spent=spent,
            percent=percent,
            remaining=remaining
        ))

        total_budgeted += budgeted
        total_spent += spent

    total_percent = int((total_spent / total_budgeted * 100)) if total_budgeted > 0 else 0
    total_remaining = total_budgeted - total_spent

    period_str = start_date.strftime("%Y-%m")

    return DashboardSummary(
        period=period_str,
        period_type=period_type,
        categories=categories_summary,
        total_budgeted=total_budgeted,
        total_spent=total_spent,
        total_percent=total_percent,
        total_remaining=total_remaining
    )