from typing import Iterator
from sqlalchemy.orm import Session
from app.database import SessionLocal

# Request get a fresh database session, and it closes after response.
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()