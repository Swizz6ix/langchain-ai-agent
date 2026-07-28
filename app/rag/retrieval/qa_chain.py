from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from app.rag.prompt_template.prompt_temp import prompt_temp
from app.prompts.qa import QA_PROMPT
from app.llm.provider_gemini import get_llm

def get_stuff_chain():
    stuff_chain = create_stuff_documents_chain(
        get_llm(), 
        prompt_temp(QA_PROMPT)
    )

    return stuff_chain
