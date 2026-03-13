from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.plaid import ExchangeTokenRequest, LinkTokenResponse, PlaidItemResponse
from app.services.plaid_service import create_link_token, exchange_public_token

router = APIRouter(prefix="/plaid", tags=["plaid"])


@router.post("/link-token", response_model=LinkTokenResponse)
def get_link_token(current_user: User = Depends(get_current_user)):
    link_token = create_link_token(current_user.id)
    return LinkTokenResponse(link_token=link_token)


@router.post("/exchange-token", response_model=PlaidItemResponse, status_code=status.HTTP_201_CREATED)
def exchange_token(body: ExchangeTokenRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plaid_item = exchange_public_token(db, current_user.id, body.public_token)
    return plaid_item
