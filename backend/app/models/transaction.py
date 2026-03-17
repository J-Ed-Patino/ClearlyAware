import uuid
from datetime import datetime, timezone, date
from sqlalchemy import String, DateTime, Date, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    plaid_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("plaid_items.id"), nullable=False)
    plaid_transaction_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pending: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
