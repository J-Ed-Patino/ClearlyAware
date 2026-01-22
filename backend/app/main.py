from fastapi import FastAPI
from app.routers.auth import router as auth_router

app = FastAPI( title="ClearlyAware", description="Personal budget tracker with bank integration", version="0.1.0" )

app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def check_health():
    return {"status": "working"}
 