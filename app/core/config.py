from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: SecretStr = Field(validation_alias="OPENROUTER_API_KEY")
    pinecore_api_key: str = Field(validation_alias="PINECONE_API_KEY")
    google_api_key: SecretStr = Field(validation_alias="GOOGLE_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
