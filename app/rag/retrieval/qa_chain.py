from typing import Any

from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from app.llm.provider_gemini import get_llm
from app.prompts.qa import QA_PROMPT
from app.rag.prompt_template.prompt_temp import prompt_temp


def get_stuff_chain() -> Any:
    stuff_chain = create_stuff_documents_chain(get_llm(), prompt_temp(QA_PROMPT))

    return stuff_chain
