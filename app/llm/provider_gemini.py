from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm() -> Any:
    return ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)
