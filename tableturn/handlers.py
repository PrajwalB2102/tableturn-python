"""The one place errors become HTTP: every domain refusal and every validation failure is application/problem+json
built by `problem`."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from tableturn.errors import NoSuchBranch, NoSuchTable


def problem(status: int, error_type: str, title: str, detail: str):
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={
            "type": error_type,
            "title": title,
            "status": status,
            "detail": detail,
        },
    )


async def validation_handler(
    request: Request, exc: RequestValidationError
):
    return problem(
        400,
        "/errors/validation",
        "Validation Error",
        "One or more request parameters are invalid.",
    )


async def http_handler(
    request: Request, exc: StarletteHTTPException
):
    if exc.status_code == 404:
        return problem(
            404,
            "/errors/not-found",
            "Not Found",
            "The requested resource was not found.",
        )

    return problem(
        exc.status_code,
        f"/errors/http-{exc.status_code}",
        "HTTP Error",
        str(exc.detail),
    )


async def branch_handler(request: Request, exc: NoSuchBranch):
    return problem(
        404,
        "/errors/no-such-branch",
        "Branch Not Found",
        str(exc),
    )


async def table_handler(request: Request, exc: NoSuchTable):
    return problem(
        404,
        "/errors/no-such-table",
        "Table Not Found",
        str(exc),
    )
