import os
from typing import Any

from langchain.tools import tool
from tavily import TavilyClient


def get_tavily() -> Any:
    return TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


@tool
def web_search(query: str, num_results: int = 5, min_score: float = 0.70) -> list[dict[str, Any]]:
    """
    Perform a web search using the provided query and return a list of search results.

    Args:
        query (str): The search query.
        num_results (int): The number of search results to return. Default is 5.

    Returns:
        list: A list of search result URLs.
    """
    client = get_tavily()

    response = client.search(
        query=query,
        search_depth="advanced",
        # include_answer = "advanced",
        max_results=num_results,
    )

    return [
        {
            "title": result["title"],
            "content": result["content"],
            "url": result["url"],
            "score": result["score"],
        }
        for result in response["results"]
        if result["score"] >= min_score
    ]
