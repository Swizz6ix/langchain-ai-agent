from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: SecretStr = Field(validation_alias="OPENROUTER_API_KEY")
    pinecore_api_key: str = Field(validation_alias="PINECONE_API_KEY")
    google_api_key: SecretStr = Field(validation_alias="GOOGLE_API_KEY")
    invite_secret: str = Field(validation_alias="INVITE_SECRET")
    jwt_secret: str = Field(validation_alias="JWT_SECRET")
    jwt_algorithm: str = Field(validation_alias="JWT_ALGORITHM")
    jwt_iss: str = Field(validation_alias="JWT_ISSUER")
    jwt_aud: str = Field(validation_alias="JWT_AUDIENCE")
    access_token_expire_minutes: int = Field(validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    redis_host: str = Field(validation_alias="REDIS_HOST")
    redis_port: int = Field(validation_alias="REDIS_PORT")

    database_url: str = Field(validation_alias="DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
