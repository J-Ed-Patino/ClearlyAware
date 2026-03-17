from sqlalchemy.orm import Session

from app.models.plaid_item import PlaidItem
from app.models.transaction import Transaction
from app.services.plaid_service import get_plaid_client
from plaid.model.transactions_sync_request import TransactionsSyncRequest

# Maps Plaid's primary category to our category names
PLAID_CATEGORY_MAP = {
    "FOOD_AND_DRINK": "Dining",
    "TRAVEL": "Transport",
    "TRANSPORTATION": "Transport",
    "ENTERTAINMENT": "Entertainment",
    "GENERAL_MERCHANDISE": "Shopping",
    "MEDICAL": "Health",
    "PERSONAL_CARE": "Health",
    "HOME_IMPROVEMENT": "Utilities",
    "UTILITIES": "Utilities",
    "GROCERIES": "Groceries",
    "TRANSFER_IN": "Other",
    "TRANSFER_OUT": "Other",
    "LOAN_PAYMENTS": "Other",
    "BANK_FEES": "Other",
    "INCOME": "Other",
    "GOVERNMENT_AND_NON_PROFIT": "Other",
}


def map_category(plaid_primary: str | None) -> str:
    if not plaid_primary:
        return "Other"
    return PLAID_CATEGORY_MAP.get(plaid_primary, "Other")


def sync_transactions(db: Session, plaid_item: PlaidItem) -> dict:
    client = get_plaid_client()
    added_count = 0
    modified_count = 0
    removed_count = 0

    # Use stored cursor if we have one, otherwise Plaid starts from the beginning
    cursor = plaid_item.cursor

    # Plaid may paginate results — keep fetching until has_more is False
    has_more = True
    while has_more:
        request = TransactionsSyncRequest(access_token=plaid_item.access_token)
        if cursor:
            request = TransactionsSyncRequest(access_token=plaid_item.access_token, cursor=cursor)

        response = client.transactions_sync(request)

        # Insert new transactions
        for transaction in response["added"]:
            existing = db.query(Transaction).filter(
                Transaction.plaid_transaction_id == transaction["transaction_id"]
            ).first()
            if not existing:
                plaid_category = transaction.get("personal_finance_category", {}).get("primary")
                db.add(Transaction(
                    user_id=plaid_item.user_id,
                    plaid_item_id=plaid_item.id,
                    plaid_transaction_id=transaction["transaction_id"],
                    amount=transaction["amount"],
                    date=transaction["date"],
                    name=transaction["name"],
                    category_name=map_category(plaid_category),
                    pending=transaction["pending"],
                ))
                added_count += 1

        # Update modified transactions
        for transaction in response["modified"]:
            existing = db.query(Transaction).filter(
                Transaction.plaid_transaction_id == transaction["transaction_id"]
            ).first()
            if existing:
                plaid_category = transaction.get("personal_finance_category", {}).get("primary")
                existing.amount = transaction["amount"]
                existing.name = transaction["name"]
                existing.pending = transaction["pending"]
                existing.category_name = map_category(plaid_category)
                modified_count += 1

        # Remove deleted transactions
        for transaction in response["removed"]:
            existing = db.query(Transaction).filter(
                Transaction.plaid_transaction_id == transaction["transaction_id"]
            ).first()
            if existing:
                db.delete(existing)
                removed_count += 1

        cursor = response["next_cursor"]
        has_more = response["has_more"]

    # Save the latest cursor back to the PlaidItem for next sync
    plaid_item.cursor = cursor
    db.commit()

    return {"added": added_count, "modified": modified_count, "removed": removed_count}
