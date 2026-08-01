from dataclasses import dataclass


@dataclass
class RequestContext:
    request_id: str
    user_id: str | None = None
    session_id: str | None = None
