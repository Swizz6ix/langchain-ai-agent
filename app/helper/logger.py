import logging

from app.core.contextvars import request_context

logger = logging.getLogger(__name__)

def log_info(message, **kwargs):
    ctx = request_context.get()

    logger.info(
        message,
        extra = {
            "request_id": ctx.request_id,
            "user_id": ctx.user_id,
            "session_id": ctx.session_id,
            **kwargs
        }
    )