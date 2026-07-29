from functools import lru_cache
from typing import Any

from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from app.llm.provider_openrouter import get_llm
from app.prompts.research import RESEARCH_PROMPT
from app.tools.text_summarizer import text_summarizer
from app.tools.web_search import web_search

tools = [
    web_search,
    text_summarizer,
]


@lru_cache(maxsize=1)
def research_agent() -> CompiledStateGraph[Any, Any, Any, Any]:
    return create_agent(model=get_llm(), tools=tools, system_prompt=RESEARCH_PROMPT)
