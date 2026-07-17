from unittest.mock import Mock

from app.tools.web_search import web_search


def test_web_search(mocker):
    mock_client = Mock()

    mock_client.search.return_value = {"results": [{"url": "https://example.com"}]}

    mocker.patch("app.tools.web_search.get_tavily", return_value=mock_client)

    result = web_search.invoke({"query": "LangChain"})

    assert len(result) == 1
    assert result[0] == "https://example.com"
