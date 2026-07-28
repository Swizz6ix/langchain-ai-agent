from typing import Any

from langsmith import traceable

from app.rag.retrieval.document_retriever import documents_retriever
from app.rag.retrieval.rerank_documents import rerank_documents
from app.rag.retrieval.rewrite_query import rewrite_query


@traceable(run_type="retriever", name="multi_query_retriever")
def multi_query_retriever(question: str, source: str | None = None, top_n: int = 5) -> Any:
    """
    Rewrite query into multiple versions, retrieve from all, deduplicate, rerank
    """
    queries = rewrite_query(question)
    docs = documents_retriever(
        queries,
        source,
    )

    docs = rerank_documents(question, docs)

    return docs
