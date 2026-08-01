from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: str
    email: str
    role: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRequest(BaseModel):
    access_token: str
    token_type: str = "Bearer"
