from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.home import router as root
from app.api.rag_assistant import router as rag_assistant
from app.api.tool_assistant import router as tool_assistant

load_dotenv()

app = FastAPI(title="Langchain AI Agent")

app.include_router(root)

app.include_router(tool_assistant, prefix="/api/v1")
app.include_router(rag_assistant, prefix="/api/v1")

app.include_router(health_router)
