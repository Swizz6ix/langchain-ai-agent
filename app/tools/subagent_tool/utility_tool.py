from typing import Any

from langchain.tools import tool

from app.agents.subagents.utility_agent import utility_agent


@tool
def utility_tool(request: str) -> Any:
    """
    Get weather report and forecast and also perform mathematical operations
    Use the Calculator whenever mathematical computation, arithmetic,
    percentages, conversions, or numerical reasoning is required.
    Use the Weather tool whenever the user requests weather forecasts
    """
    agent = utility_agent()

    result = agent.invoke({"messages": [{"role": "user", "content": request}]})

    return result["messages"][-1].text
