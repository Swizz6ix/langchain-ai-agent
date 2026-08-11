from pydantic import EmailStr, BaseModel

class UserResponse(BaseModel):
    id: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }