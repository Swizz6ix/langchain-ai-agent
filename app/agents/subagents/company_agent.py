from functools import lru_cache
from typing import Any

from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from app.llm.provider_openrouter import get_llm
from app.prompts.company import COMPANY_PROMPT
from app.tools.company_rag import company_rag

tools = [company_rag]


@lru_cache(maxsize=1)
def company_agent() -> CompiledStateGraph[Any, Any, Any, Any]:
    return create_agent(model=get_llm(), tools=tools, system_prompt=COMPANY_PROMPT)
