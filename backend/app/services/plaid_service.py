from uuid import UUID

import plaid
from plaid.api import plaid_api
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from sqlalchemy.orm import Session

from app.config import settings
from app.models.plaid_item import PlaidItem

ENV_MAP = {
    "sandbox": plaid.Environment.Sandbox,
    "production": plaid.Environment.Production,
}


def get_plaid_client() -> plaid_api.PlaidApi:
    configuration = plaid.Configuration(
        host=ENV_MAP[settings.plaid_env],
        api_key={
            "clientId": settings.plaid_client_id,
            "secret": settings.plaid_secret,
        },
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)


def create_link_token(user_id: UUID) -> str:
    client = get_plaid_client()
    request = LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name="ClearlyAware",
        country_codes=[CountryCode("US")],
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id=str(user_id)),
    )
    response = client.link_token_create(request)
    return response["link_token"]


def exchange_public_token(db: Session, user_id: UUID, public_token: str) -> PlaidItem:
    client = get_plaid_client()
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)

    access_token = response["access_token"]
    item_id = response["item_id"]

    plaid_item = PlaidItem(
        user_id=user_id,
        access_token=access_token,
        item_id=item_id,
    )
    db.add(plaid_item)
    db.commit()
    db.refresh(plaid_item)
    return plaid_item
