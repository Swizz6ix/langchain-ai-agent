from typing import Any


def text_summarizer(text: str, max_length: int=100) -> Any :
    """
    Summarizes the input text to a specified maximum length.

    Parameters:
    text (str): The input text to be summarized.
    max_length (int): The maximum length of the summary.

    Returns:
    str: The summarized text.
    """
    # Placeholder for actual summarization logic
    # In a real implementation, you would use an AI model or algorithm here
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length] + "..."
