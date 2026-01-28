from app.database import SessionLocal
from app.models.category import Category

CATEGORIES = [
    {"name": "Groceries", "plaid_primary": "FOOD_AND_DRINK", "plaid_detailed": "FOOD_AND_DRINK_GROCERIES"},
    {"name": "Dining", "plaid_primary": "FOOD_AND_DRINK", "plaid_detailed": "FOOD_AND_DRINK_RESTAURANTS"},
    {"name": "Transport", "plaid_primary": "TRANSPORTATION", "plaid_detailed": None},
    {"name": "Utilities", "plaid_primary": "UTILITIES", "plaid_detailed": None},
    {"name": "Entertainment", "plaid_primary": "ENTERTAINMENT", "plaid_detailed": None},
    {"name": "Shopping", "plaid_primary": "SHOPPING", "plaid_detailed": None},
    {"name": "Health", "plaid_primary": "HEALTHCARE", "plaid_detailed": None},
    {"name": "Other", "plaid_primary": None, "plaid_detailed": None},
    ]

def seed_categories():
    db = SessionLocal()
    try:
        for cat in CATEGORIES:
            exists = db.query(Category).filter(Category.name == cat["name"]).first()
            if not exists:
                db.add(Category(**cat))
        db.commit()
        print("Category seeded.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_categories()
            