from concurrent.futures import ThreadPoolExecutor
from typing import List
from langchain_core.documents import Document
from app.rag.retrieval.get_retriever import get_retriever

def documents_retriever(queries, source=None, top_n=5) -> List[Document]:
    """
    Rewrite query into multiple versions, retrieve from all, deduplicate, rerank
    """
    retriever = get_retriever(source)

    def retrieve(q):
        return retriever.invoke(q)

    with ThreadPoolExecutor(max_workers=len(queries)) as executor:
        results = list(executor.map(retrieve, queries))

    docs = []
    seen_ids = set()

    for batch in results:
        for doc in batch:
        # for doc in retriever.invoke(q, config=RunnableConfig(run_name=f"retrieve_for_rewrite")):
            doc_id = doc.metadata["doc_id"]
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                docs.append(doc)
                
    return docs[:top_n * 2]