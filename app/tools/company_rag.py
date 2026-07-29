from typing import Any

from langchain.tools import tool
from pydantic import BaseModel, Field

from app.rag.retrieval.question_answer import answer_question


class CompanyInput(BaseModel):
    """Input for company queries."""

    question: str = Field(description="user query")
    source: str = Field(description="Optional, filter for the vector store to search")


@tool("company", description="Searches vector store for relevant company data")
def company_rag(question: str, source: str) -> Any:
    """
    Searches pinecore for relevant company data

    Args:
        question (str): user's query
        source (str): Optional filter, the area the user is seeking company knowledge
            It can either be 'faq' or 'handbook'

    Returns:
        dict: containing the user's question and the appropriate answer
    """

    return answer_question(question, source)
