from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.assistant import get_agent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat")
async def chat(request: ChatRequest) -> dict[str, Any]:
    agent = get_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": request.message}]})

    final_message = result["messages"][-1]

    return {"response": final_message.content}
