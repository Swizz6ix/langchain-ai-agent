from app.models.base import Base
from pydantic import BaseModel, EmailStr



class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str |  None = None
    token_type: str = "Bearer"
