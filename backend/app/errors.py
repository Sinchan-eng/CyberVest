"""Consistent error envelope (docs/05-api-specification.md sections 7-8)."""

from __future__ import annotations

import uuid

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

CODE_STATUS = {
    "VALIDATION_ERROR": 422,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "CONFLICT": 409,
    "DATABASE_ERROR": 500,
    "INTERNAL_ERROR": 500,
    "AI_UNAVAILABLE": 503,
    "SERVICE_UNAVAILABLE": 503,
}

STATUS_CODE = {
    400: "BAD_REQUEST",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    500: "INTERNAL_ERROR",
    503: "SERVICE_UNAVAILABLE",
}


class APIError(Exception):
    def __init__(self, code: str, message: str, details: list | None = None):
        self.code = code
        self.message = message
        self.details = details or []
        self.http_status = CODE_STATUS.get(code, 500)


def _request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


def _envelope(code: str, message: str, details: list | None = None) -> dict:
    body = {
        "error": {
            "code": code,
            "message": message,
            "request_id": _request_id(),
        }
    }
    if details:
        body["error"]["details"] = details
    return body


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(APIError)
    async def _api_error(_: Request, exc: APIError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_status,
            content=_envelope(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {"field": ".".join(str(p) for p in e["loc"][1:]), "message": e["msg"]}
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_envelope("VALIDATION_ERROR", "Request validation failed", details),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = STATUS_CODE.get(exc.status_code, "INTERNAL_ERROR")
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return JSONResponse(status_code=exc.status_code, content=_envelope(code, message))

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        # Never leak internal exception details to the client.
        return JSONResponse(
            status_code=500,
            content=_envelope("INTERNAL_ERROR", "An unexpected error occurred"),
        )
