from fastapi import FastAPI
# Load all models so SQLAlchemy sees them
from app.models.user import User
from app.models.category import Category
from app.models.budget import Budget
from app.routers.auth import router as auth_router
from app.routers.budgets import router as budget_router

PREFIX = "/api/v1"

app = FastAPI( title="ClearlyAware", description="Personal budget tracker with bank integration", version="0.1.0" )

app.include_router(auth_router, prefix=PREFIX)
app.include_router(budget_router, prefix=PREFIX )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def check_health():
    return {"status": "working"}
 