from langchain_core.runnables import RunnableConfig
from langsmith import traceable
from app.rag.retrieval.multi_query_retriever import multi_query_retriever
from app.rag.retrieval.qa_chain import get_stuff_chain

stuff_chain = get_stuff_chain()
@traceable(run_type="chain", name="answer_question")
def answer_question(question: str, source=None):
    docs = multi_query_retriever(question, source)
    return stuff_chain.invoke(
        {
            "context": docs,
            "question": question
        },
        config=RunnableConfig(
            run_name="qa_generation",
            tags=["production" if not source else f"source:{source}"],
            metadata={
                "query": question,
                "source_filter": source,
                "num_docs": len(docs)
            }
        )
    )
