from typing import Any

from langchain.tools import tool

from app.agents.subagents.research_agent import research_agent


@tool
def research_tool(request: str) -> Any:
    """
    Search the internet using
    Use this whenever the user wants current or external
    information from the internet
    """

    agent = research_agent()

    result = agent.invoke({"messages": [{"role": "user", "content": request}]})

    return result["messages"][-1]
