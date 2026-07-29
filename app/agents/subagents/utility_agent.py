from functools import lru_cache
from typing import Any

from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from app.llm.provider_openrouter import get_llm
from app.prompts.utility import UTILITY_PROMPT
from app.tools.calculator import calculator
from app.tools.get_weather import get_weather

tools = [
    calculator,
    get_weather,
]


@lru_cache(maxsize=1)
def utility_agent() -> CompiledStateGraph[Any, Any, Any, Any]:
    return create_agent(model=get_llm(), tools=tools, system_prompt=UTILITY_PROMPT)
