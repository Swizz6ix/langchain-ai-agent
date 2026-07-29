from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.supervisor_agent import supervisor_agent

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class chatResponse(BaseModel):
    response: str


@router.post("/chat")
async def chat(query: ChatRequest) -> dict[str, Any]:
    agent = supervisor_agent()
    result = agent.invoke({
        "messages": [{
            "role": "user", 
            "content": query
        }]
    })

    response = result["messages"][-1]

    return {"response": response.content}
