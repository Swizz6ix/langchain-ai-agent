from typing import Any

from langchain.tools import tool

from app.agents.subagents.company_agent import company_agent


@tool
def company_tool(request: str) -> Any:
    """
    Answer questions using the organization's internal knowledge base.
    """
    agent = company_agent()

    result = agent.invoke({"messages": [{"role": "user", "content": request}]})

    return result["messages"][-1]
