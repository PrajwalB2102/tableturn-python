
"""Database engine and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tableturn.models import Base, Table
from tableturn.settings import Settings

engine = None
SessionLocal = None


def configure_database(settings: Settings) -> None:
    """Build the engine using the current environment settings."""
    global engine, SessionLocal

    options = {}
    connect_args = {}

    if settings.database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        if settings.database_url in ("sqlite://", "sqlite:///:memory:"):
            options["poolclass"] = StaticPool

    if engine is not None:
        engine.dispose()

    engine = create_engine(
        settings.database_url,
        connect_args=connect_args,
        **options,
    )
    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )


def create_schema() -> None:
    """Create the registered SQLAlchemy tables."""
    if engine is None:
        configure_database(Settings())

    _ = Table
    Base.metadata.create_all(bind=engine)


def get_db():
    """Provide a session for API routes."""
    if SessionLocal is None:
        configure_database(Settings())

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
