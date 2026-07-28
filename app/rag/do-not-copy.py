import re
import os
import getpass
import hashlib
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_core.prompts import ChatPromptTemplate
from app.prompts.rewrite_query import REWRITE_PROMPT
from app.prompts.qa import QA_PROMPT
from app.prompts.system import SYSTEM_PROMPT
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()


if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API Key for Google Gemini: ")

if not os.environ.get("PINECONE_API_KEY"):
    os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter API Key for PINECONE STORE: ")

if not os.environ.get("COHERE_API_KEY"):
    os.environ["COHERE_API_KEY"] = getpass.getpass("Enter API Key for COHERE: ")

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


faq_path = Path("app/assets/main_frequently-asked-questions-about-your-gm-supplier-discount.pdf")
handBook_path = Path("app/assets/Employee-Handbook.pdf")

if not faq_path.exists():
    raise FileNotFoundError(f"FAQ PDF not found: {faq_path.resolve()}")

if not handBook_path.exists():
    raise FileNotFoundError(f"Handbook PDF not found: {handBook_path.resolve()}")

faq = PdfReader(faq_path)
handBook = PdfReader(handBook_path)

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    temperature = 0
)


pages = [
    {
        "page": page_num,
        "text": page.extract_text() or ""
    }

    for page_num, page in enumerate(faq.pages)
]

faq_docs = [
    Document(
        page_content=section.strip(),
        metadata={
            "source": "faq",
            "page": page["page"],
            "section": i
        }
    )

    for page in pages
    for i, section in enumerate(re.split(r"(?=Q\.)", page["text"]))
    if section.strip()
]

handbook_docs = []

for page_num, page in enumerate(handBook.pages):
    text = page.extract_text() or ""

    if text.strip():
        handbook_docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": "handbook",
                    "page": page_num
                }
            )
        )

# print(len(faq_docs))
# print(docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

handbook_chunks = splitter.split_documents(handbook_docs)
faq_chunks = splitter.split_documents(faq_docs)

# print(chunks)
# print(len(handBook_chunks))


# print("toal length", len(faq_docs))
# print(faq_docs[0].metadata)
# print(faq_docs[-1].metadata)


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# vector = embeddings.embed_query(docs[0].page_content)

# print(vector[:10])



pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index_name = "company-knowledge"
index = pc.Index(index_name)

# print(pinecone.list_indexes())

# vector_store_customer = PineconeVectorStore.from_documents(
#     documents=faq_chunks,
#     embedding=embeddings,
#     index_name="company-knowledge",
#     namespace="customer"
# )

# vector_store_employee = PineconeVectorStore.from_documents(
#     documents=handBook_chunks,
#     embedding=embeddings,
#     index_name="company-knowledge",
#     namespace="employee"
# )

for doc in faq_chunks:
    doc.id = hashlib.sha256(
        f"{doc.metadata['source']}-{doc.metadata['page']}-{doc.metadata['section']}-{doc.page_content}".encode()
    ).hexdigest()

for doc in handbook_chunks:
    doc.id = hashlib.sha256(
        f"{doc.metadata['source']}-{doc.metadata['page']}-{doc.page_content}".encode()
    ).hexdigest()


vector_store = PineconeVectorStore(
    index_name = index_name,
    embedding = embeddings,
)


vector_store.add_documents(faq_chunks + handbook_chunks)


retriever_all = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 10}
)

retriever_faq = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {
        "k": 10,
        "filter": {
            "source": "faq"
        }
    }
)

retriever_handbook = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {
        "k": 10,
        "filter": {
            "source":"handbook"
        }
    }
) 

def get_retriever(source=None):
    kwargs = {"k": 20}

    if source:
        kwargs["filter"] = {"source": source}

    return vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = kwargs
    )

rephase_query = ChatPromptTemplate.from_messages([
    (
        "system",
        REWRITE_PROMPT,
    ),
    (
        "human",
        "{question}"
    )
])

def rewrite_query(question: str) -> List[str]:
    """Generate 3 query variations and return them as a list"""
    chain = rephase_query | llm | StrOutputParser()
    result = chain.invoke({"question": question})

    print("results..query>>", result)

    # Parse numbered List
    queries = [line.strip() for line in result.split("\n") if line.strip()]

    # Remove numbering (1. 2. 3.)
    queries = [re.sub(r"^\d+\.\s*", "", q) for q in queries]

    # Always include the original question
    if question not in queries:
        queries.insert(0, question)
    print("queries", queries)
    
    return queries




user_query = "How do I get a discount"


# query_rewriter = rephase_query | llm
# response = query_rewriter.invoke({
#     "question": user_query
# })

# if isinstance(response.content, str):
#     query = response.content

# else:
#     query = "".join(
#         part["text"]
#         for part in response.content
#         if part.get("type") == "text"
#     )

# print("query ==>", query)



results_all = retriever_all.invoke("How do I get a discount")
results_faq = retriever_faq.invoke("How do I get a discount")
results_hb = retriever_handbook.invoke("What is the standard working hours")

for doc in results_all:
    print("all =>", doc.metadata)
    print("all =>", doc.page_content)
    print("=" * 80)

for doc in results_faq:
    print("faq =>", doc.metadata)
    print("faq =>", doc.page_content)
    print("=" * 80)


for doc in results_hb:
    print("hb =>", doc.metadata)
    print("hb =>", doc.page_content)
    print("=" * 80)

retriever = get_retriever()

compressor = CohereRerank( model="rerank-v4.0-pro", top_n = 5)
compression_retriever = ContextualCompressionRetriever(
    base_compressor = compressor,
    base_retriever = retriever
)

# results = compression_retriever.invoke(query)

qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        QA_PROMPT,
    ),
    (
        "human",
        "{question}"
    )
])

def format_docs(docs: List[Document]) -> str:
    """
    Format retrieved documents into a single context string
    """
    formatted = []

    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        formatted.append(f"[Document {i} | Source: {source} | Page: {page}]\n{doc.page_content}")
    return "\n\n--\n\n".join(formatted)

# Multi_query retriever
def multi_query_retriever(question: str, source=None, top_n=5) -> List[Document]:
    """
    Rewrite query into multiple versions, retrieve from all, deduplicate rerank
    """
    queries = rewrite_query(question)
    retriever = compression_retriever

    all_docs = []
    seen_ids = set()

    for q in queries:
        docs = retriever.invoke(q)
        for doc in docs:
            if doc.id not in seen_ids:
                seen_ids.add(doc.id)
                all_docs.append(doc)
    print("docs", all_docs)
    return all_docs[:top_n * 2]

def create_qa_chain(source=None):
    """Returns a runnable chain: question -> docs -> answer."""

    def retrive_and_format(question: str):
        docs = multi_query_retriever(question, source=source, top_n=5)
        return {"context": format_docs(docs), "docs": docs, "question": question}

    chain = (
        RunnablePassthrough() | retrive_and_format | qa_prompt | llm | StrOutputParser()
    )

    return chain

qa_chain = create_qa_chain()

answer = qa_chain.invoke(user_query)
print("ANSWERS>>>>>", answer)


# qa_chain = create_stuff_documents_chain(
#     llm,
#     qa_prompt
# )

# answer = qa_chain.invoke({
#     "context": results,
#     "question": user_query
# })

# print("rerank",results)
# print("QA", answer)

