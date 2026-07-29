from functools import lru_cache
from typing import Any

from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from app.llm.provider_openrouter import get_llm
from app.prompts.supervisor import SUPERVISOR_PROMPT
from app.tools.subagent_tool.company_tool import company_tool
from app.tools.subagent_tool.research_tool import research_tool
from app.tools.subagent_tool.utility_tool import utility_tool

tools = [
    research_tool,
    utility_tool,
    company_tool,
]


@lru_cache(maxsize=1)
def supervisor_agent() -> CompiledStateGraph[Any, Any, Any, Any]:
    return create_agent(model=get_llm(), tools=tools, system_prompt=SUPERVISOR_PROMPT)
