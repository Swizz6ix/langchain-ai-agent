from langsmith import traceable
from app.rag.retrieval.reranker import get_reranker

reranker = get_reranker()
@traceable(run_type="retriever", name="rerank_documents")
def rerank_documents(question, docs):
    compressed = reranker.compress_documents(
        documents=docs,
        query=question,
    )

    return compressed