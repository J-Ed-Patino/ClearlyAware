from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.middleware.auth import get_current_user
from app.models.plaid_item import PlaidItem
from app.models.user import User
from app.schemas.plaid import ExchangeTokenRequest, LinkTokenResponse, PlaidItemResponse
from app.services.plaid_service import create_link_token, exchange_public_token
from app.services.transaction import sync_transactions

router = APIRouter(prefix="/plaid", tags=["plaid"])


@router.post("/link-token", response_model=LinkTokenResponse)
def get_link_token(current_user: User = Depends(get_current_user)):
    link_token = create_link_token(current_user.id)
    return LinkTokenResponse(link_token=link_token)


@router.post("/exchange-token", response_model=PlaidItemResponse, status_code=status.HTTP_201_CREATED)
def exchange_token(body: ExchangeTokenRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plaid_item = exchange_public_token(db, current_user.id, body.public_token)
    return plaid_item


@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    webhook_type = body.get("webhook_type")
    webhook_code = body.get("webhook_code")
    item_id = body.get("item_id")

    if webhook_type == "TRANSACTIONS" and webhook_code == "SYNC_UPDATES_AVAILABLE":
        plaid_item = db.query(PlaidItem).filter(PlaidItem.item_id == item_id).first()
        if plaid_item:
            sync_transactions(db, plaid_item)

    return {"status": "ok"}


@router.post("/sync")
def manual_sync(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(PlaidItem).filter(PlaidItem.user_id == current_user.id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No linked bank accounts found.")
    results = []
    for item in items:
        result = sync_transactions(db, item)
        results.append({"item_id": item.item_id, **result})
    return results
