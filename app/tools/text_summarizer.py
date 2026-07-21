from typing import Any

from langchain.tools import tool

from app.llm.provider import get_llm


@tool("summarize", description="Performs text summarization")
def text_summarizer(text: str, max_length: int = 100) -> Any:
    """
    Summarizes the input text to a specified maximum length.

    Parameters:
    text (str): The input text to be summarized.
    max_length (int): The maximum length of the summary.

    Returns:
    str: The summarized text.
    """

    model = get_llm()

    messages = [
        (
            "system",
            f"""You are a helpful assistant that provide short summary of text. 
            Summarize the user text in more than {max_length} words
            """,
        ),
        ("user", text),
    ]

    response = model.invoke(messages)
    return response.content
