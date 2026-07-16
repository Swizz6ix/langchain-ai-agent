def web_search(query: str, num_results: int = 5) -> list[str]:
    """
    Perform a web search using the provided query and return a list of search results.

    Args:
        query (str): The search query.
        num_results (int): The number of search results to return. Default is 5.

    Returns:
        list: A list of search result URLs.
    """
    # Placeholder for actual web search implementation
    # This function should interact with a web search API or service
    # For demonstration purposes, we will return a mock list of URLs
    mock_results = [
        f"https://example.com/search?q={query}&result={i}" for i in range(1, num_results + 1)
    ]
    return mock_results
