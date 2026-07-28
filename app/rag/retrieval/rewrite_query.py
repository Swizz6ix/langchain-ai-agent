import re

from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable

from app.llm.provider_gemini import get_llm
from app.prompts.rewrite_query import REWRITE_PROMPT
from app.rag.prompt_template.prompt_temp import prompt_temp

rephase_query = prompt_temp(REWRITE_PROMPT)


@traceable(run_type="llm", name="query_rewriter")
def rewrite_query(question: str) -> list[str]:
    """Generate 3 query variations and return them as a list"""
    chain = rephase_query | get_llm() | StrOutputParser()
    result = chain.invoke({"question": question})

    # Parse numbered List
    queries = [line.strip() for line in result.split("\n") if line.strip()]

    # Remove numbering (1. 2. 3.)
    queries = [re.sub(r"^\d+\.\s*", "", q) for q in queries]

    # Always include the original question
    if question not in queries:
        queries.insert(0, question)

    return queries
