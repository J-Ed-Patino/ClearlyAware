from uuid import UUID
from pydantic import BaseModel


class ExchangeTokenRequest(BaseModel):
    public_token: str


class LinkTokenResponse(BaseModel):
    link_token: str


class PlaidItemResponse(BaseModel):
    id: UUID
    item_id: str
    institution_name: str | None

    class Config:
        from_attributes = True
