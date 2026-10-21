
"""Idempotent CSV seeding for dining tables."""

import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from tableturn.models import Table
from tableturn.settings import Settings


def seed_tables(db: Session, settings: Settings) -> None:
    """Seed the floor only when the tables table is empty."""
    existing = db.scalar(select(Table.id).limit(1))
    if existing is not None:
        return

    csv_path = Path(settings.seed_dir) / "tables.csv"

    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Table seed file not found: {csv_path.resolve()}"
        )

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        required = {"no", "seats", "section"}

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "tables.csv must contain no, seats, and section columns"
            )

        rows = list(reader)

    if len(rows) != 22:
        raise ValueError(f"Expected 22 tables, found {len(rows)}")

    tables = [
        Table(
            no=row["no"].strip(),
            branch=(row.get("branch") or "Baner").strip(),
            seats=int(row["seats"]),
            section=row["section"].strip(),
        )
        for row in rows
    ]

    db.add_all(tables)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
