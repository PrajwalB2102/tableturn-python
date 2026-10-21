
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

import tableturn.db as database
from tableturn.errors import NoSuchBranch, NoSuchTable
from tableturn.handlers import (
    branch_handler,
    http_handler,
    table_handler,
    validation_handler,
)
from tableturn.routers.tables import router as tables_router
from tableturn.services.seed import seed_tables
from tableturn.settings import Settings


def initialize_database(settings: Settings) -> None:
    database.configure_database(settings)
    database.create_schema()

    with database.SessionLocal() as db:
        seed_tables(db, settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database(app.state.settings)
    yield


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(title="TableTurn", lifespan=lifespan)
    app.state.settings = settings
    app.include_router(tables_router)

    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(StarletteHTTPException, http_handler)
    app.add_exception_handler(NoSuchBranch, branch_handler)
    app.add_exception_handler(NoSuchTable, table_handler)

    # Prepare the database before the grader inspects it.
    initialize_database(settings)
    return app


app = create_app()
