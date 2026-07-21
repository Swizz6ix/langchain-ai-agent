from unittest.mock import Mock

from app.tools.text_summarizer import text_summarizer


def test_summarizer(mocker):
    mock_model = Mock()
    mock_model.invoke.return_value.content = "Short summary"

    mocker.patch("app.tools.text_summarizer.get_llm", return_value=mock_model)

    result = text_summarizer.invoke({"text": "A very long article"})

    assert result == "Short summary"
