from contextvars import ContextVar
from app.core.context import RequestContext

request_context: ContextVar[RequestContext] = ContextVar("request_context")