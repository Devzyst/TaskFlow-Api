import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings
from app.core.errors import ApiError


class InMemoryRateLimiter:
    """Track request timestamps per client within a sliding time window."""

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, client_id: str) -> tuple[bool, int]:
        """Return whether the request is allowed and how many requests remain."""

        now = time.monotonic()
        window_start = now - self.window_seconds
        hits = self._hits[client_id]

        while hits and hits[0] <= window_start:
            hits.popleft()

        if len(hits) >= self.max_requests:
            return False, 0

        hits.append(now)
        return True, self.max_requests - len(hits)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Reject excessive traffic before it reaches route handlers."""

    def __init__(self, app, limiter: InMemoryRateLimiter | None = None) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.limiter = limiter or InMemoryRateLimiter(
            settings.rate_limit_requests,
            settings.rate_limit_window_seconds,
        )

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        client_host = request.client.host if request.client else "anonymous"
        allowed, remaining = self.limiter.check(client_host)
        if not allowed:
            raise ApiError(
                "Rate limit exceeded. Please retry later.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                code="rate_limit_exceeded",
                details={"window_seconds": self.limiter.window_seconds},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
