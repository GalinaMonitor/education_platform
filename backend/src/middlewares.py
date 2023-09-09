import uuid
from typing import Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.logging_config import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Clear previous context variables
        structlog.contextvars.clear_contextvars()

        # Bind new variables identifying the request and a generated UUID
        structlog.contextvars.bind_contextvars(
            path=request.url.path,
            method=request.method,
            client_host=request.client.host,
            request_id=str(uuid.uuid4()),
        )

        # Make the request and receive a response
        try:
            response = await call_next(request)
        except Exception as e:
            structlog.contextvars.bind_contextvars(detail=e)
            logger.error("Server error")
            raise e

        # Bind the status code of the response
        structlog.contextvars.bind_contextvars(
            status_code=response.status_code,
        )

        detail = b"".join([s async for s in response.body_iterator])
        if 400 <= response.status_code < 500:
            structlog.contextvars.bind_contextvars(
                detail=detail.decode(),
            )
            logger.warn("Client error")
        else:
            logger.info("OK")

        return Response(
            content=detail,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
