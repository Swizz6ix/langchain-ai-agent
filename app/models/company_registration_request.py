from pydantic import BaseModel, EmailStr

class CompanyRegistrationRequest(BaseModel):
    company_name: str
    email: EmailStr
    password: str