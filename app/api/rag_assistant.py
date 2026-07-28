from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retrieval.question_answer import answer_question

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    source: str | None


class AskResponse(BaseModel):
    answer: str

@router.post("/ask")
async def ask(request: AskRequest):
    return {
        "question": request.question,
        "answer": answer_question(request.question, request.source)
    }