from pydantic_settings import BaseSettings
# app’s configuration.
class Settings(BaseSettings):
    database_url: str
    secret_key: str
    plaid_client_id: str
    plaid_secret: str
    plaid_env: str = "sandbox"

    # Connect to a .env file for environment variables
    class Config:
        env_file = ".env"

settings = Settings()