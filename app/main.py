import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.middleware import RequestContextMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat
from app.api.routes.health import router as health_router
from app.api.routes.home import router as root
from app.api.routes.rag_assistant import router as rag_assistant
from app.api.routes.tool_assistant import router as tool_assistant
from app.helper.lifespan import get_lifespan

load_dotenv()

logger = logging.getLogger(__name__)

lifespan = get_lifespan

app = FastAPI(title="Langchain AI Agent", lifespan=lifespan)

app.add_middleware(RequestContextMiddleware)

app.include_router(root)

app.include_router(auth_router, prefix="/api/v1")

app.include_router(chat, prefix="/api/v1")
app.include_router(tool_assistant, prefix="/api/v1")
app.include_router(rag_assistant, prefix="/api/v1")

app.include_router(health_router)
