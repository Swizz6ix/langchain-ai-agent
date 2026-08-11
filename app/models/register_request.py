from pydantic import BaseModel, EmailStr
from app.models.users import User


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str