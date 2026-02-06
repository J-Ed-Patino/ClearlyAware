from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.schemas.dashboard import DashboardSummary, CategorySummary


# Mock data for testing until Plaid is integrated
MOCK_TRANSACTIONS = {
    "Groceries": 320.45,
    "Dining": 187.30,
    "Transport": 95.00,
    "Utilities": 150.00,
    "Entertainment": 75.50,
    "Shopping": 225.00,
    "Health": 50.00,
    "Other": 45.00,
}


def get_dashboard_summary( db: Session, user_id: UUID, period_type: str = "monthly", start_date: date = None ) -> DashboardSummary:
    if not start_date:
        today = date.today()
        start_date = date(today.year, today.month, 1)

    budgets = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.period_type == period_type,
        Budget.start_date == start_date
    ).all()

    categories_summary = []
    total_budgeted = 0.0
    total_spent = 0.0

    for budget in budgets:
        category = db.query(Category).filter(Category.id == budget.category_id).first()
        category_name = category.name if category else "Unknown"
        
        # Mock data for now
        spent = MOCK_TRANSACTIONS.get(category_name, 0.0)
        budgeted = float(budget.amount)
        
        percent = int((spent / budgeted * 100)) if budgeted > 0 else 0
        remaining = budgeted - spent

        categories_summary.append(CategorySummary(
            category_id=str(budget.category_id),
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