import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context import RequestContext
from app.core.contextvars import request_context

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4()),
        )

        context = RequestContext(request_id = request_id)
        token = request_context.set(context)

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id

            return response

        finally:
            request_context.reset(token)
