from pydantic import BaseModel, EmailStr

class InviteRequest(BaseModel):
    email: EmailStr
    role: str | None = None
    idempotency_key: str | None = None


class BulkInviteRequest(BaseModel):
    invites: list[InviteRequest]