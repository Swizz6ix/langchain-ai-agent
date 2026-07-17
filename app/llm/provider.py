from typing import Any

from langchain_openrouter import ChatOpenRouter


def get_llm() -> Any:

    return ChatOpenRouter(model="OpenAI:gpt-oss-20b(free)", temperature=0, max_tokens=1024)
