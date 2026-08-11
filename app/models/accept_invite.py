from pydantic import BaseModel

class AcceptInviteRequest(BaseModel):
    token: str
    password: str