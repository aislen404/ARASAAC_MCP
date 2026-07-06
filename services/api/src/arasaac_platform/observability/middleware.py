import json
import logging
import time
from collections import defaultdict
from collections.abc import Awaitable, Callable
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("arasaac_platform.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        started = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        response.headers["x-request-id"] = request_id
        logger.info(
            json.dumps(
                {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
                ensure_ascii=False,
            )
        )
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: object, limit: int = 60, window_seconds: int = 60) -> None:
        super().__init__(app)  # type: ignore[arg-type]
        self._limit = limit
        self._window = window_seconds
        self._hits: defaultdict[str, list[float]] = defaultdict(list)
        self._paths = {"/api/pictograms/search", "/api/ai/plan"}

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.url.path not in self._paths:
            return await call_next(request)
        now = time.time()
        client = request.client.host if request.client else "unknown"
        hits = [stamp for stamp in self._hits[client] if now - stamp < self._window]
        if len(hits) >= self._limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Demasiadas solicitudes. Inténtalo más tarde."},
            )
        hits.append(now)
        self._hits[client] = hits
        return await call_next(request)
