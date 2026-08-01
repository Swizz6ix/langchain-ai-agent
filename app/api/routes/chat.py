from typing import Any

from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from app.agents.supervisor_agent import supervisor_agent
from app.api.dependencies import get_current_user
from app.core.contextvars import request_context

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    question: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat(query: ChatRequest, user: Any = Depends(get_current_user)) -> ChatResponse:
    agent = supervisor_agent()

    ctx = request_context.get()
    ctx.session_id = query.session_id

    input = {
        "messages": HumanMessage(content=query.question),
        "user_id": user.id,
        "session_id": ctx.session_id,
        "request_id": ctx.request_id,
    }

    result = await agent.ainvoke(input)

    response = result["messages"][-1]

    return ChatResponse(response=response.content)
