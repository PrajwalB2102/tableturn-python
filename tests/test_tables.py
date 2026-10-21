
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from tableturn.app import app, create_app
from tableturn.db import engine


def test_schema_exists_without_stored_state():
    columns = inspect(engine).get_columns("tables")
    assert "state" not in [column["name"] for column in columns]


def test_tables_are_seeded_before_first_request():
    with engine.connect() as connection:
        assert connection.execute(
            text("SELECT COUNT(*) FROM tables")
        ).scalar_one() == 22


def test_seeding_is_idempotent_across_two_starts():
    for application in (app, create_app()):
        with TestClient(application) as client:
            response = client.get("/branches/Baner/tables")
            assert response.status_code == 200
            assert len(response.json()["tables"]) == 22

        with engine.connect() as connection:
            assert connection.execute(
                text("SELECT COUNT(*) FROM tables")
            ).scalar_one() == 22
