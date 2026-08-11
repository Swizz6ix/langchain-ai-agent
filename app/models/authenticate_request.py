from pydantic import EmailStr, BaseModel
from app.models.base import Base

class LoginRequest(BaseModel):
    email: str
    password: str

