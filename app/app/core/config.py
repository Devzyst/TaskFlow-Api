"""Centralized API error types and exception handlers."""

import logging
from http import HTTPStatus
from typing import Any

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """Base exception for expected application failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = HTTPStatus.BAD_REQUEST,
        code: str = "api_error",
        details: Any | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details
        super().__init__(message)


def error_payload(
    request: Any,
    *,
    code: str,
    message: str,
    details: Any | None = None,
) -> dict[str, Any]:
    """Build a consistent error response body."""

    payload: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
            "request_id": getattr(request.state, "request_id", None),
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload


def register_exception_handlers(app: Any) -> None:
    """Attach production-safe exception handlers to the FastAPI app."""

    from fastapi import status
    from fastapi.exceptions import RequestValidationError
    from fastapi.responses import JSONResponse

    @app.exception_handler(ApiError)
    async def handle_api_error(request: Any, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_payload(request, code=exc.code, message=exc.message, details=exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Any,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_payload(
                request,
                code="validation_error",
                message="Request validation failed.",
                details=exc.errors(),
            ),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Any, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled API exception",
            extra={"request_id": getattr(request.state, "request_id", None)},
        )
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=error_payload(
                request,
                code="internal_server_error",
                message="An unexpected error occurred.",
            ),
        )
