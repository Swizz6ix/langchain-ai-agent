from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: list[BaseMessage]
    request_id: str
    user_id: str
    session_id: str