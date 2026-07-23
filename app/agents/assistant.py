from typing import Any

from langchain.agents import AgentState, create_agent
from langgraph.graph.state import CompiledStateGraph

from app.llm.provider import get_llm
from app.prompts.system import SYSTEM_PROMPT
from app.tools.calculator import calculator
from app.tools.get_weather import get_weather
from app.tools.text_summarizer import text_summarizer
from app.tools.web_search import web_search

tools = [calculator, get_weather, web_search, text_summarizer]


def get_agent() ->  CompiledStateGraph[Any, Any, Any, Any]:
    model = get_llm()
    return create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT)
