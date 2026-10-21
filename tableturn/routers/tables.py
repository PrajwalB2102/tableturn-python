
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from tableturn.db import get_db
from tableturn.errors import NoSuchBranch, NoSuchTable
from tableturn.models import Table
from tableturn.schemas import (
    Section,
    TableListOut,
    TableOut,
    TableState,
)

router = APIRouter()


def derive_state(table: Table) -> TableState:
    """A newly seeded table with no seating is free."""
    return TableState.FREE


@router.get(
    "/branches/{branch}/tables",
    response_model=TableListOut,
)
def list_tables(
    branch: str,
    section: Section | None = Query(default=None),
    state: TableState | None = Query(default=None),
    db: Session = Depends(get_db),
) -> TableListOut:
    if branch != "Baner":
        raise NoSuchBranch(branch)

    records = db.scalars(
        select(Table)
        .where(Table.branch == branch)
        .order_by(Table.no)
    ).all()

    results = []

    for table in records:
        current_state = derive_state(table)

        if section is not None and table.section != section.value:
            continue

        if state is not None and current_state != state:
            continue

        results.append(
            TableOut(
                no=table.no,
                seats=table.seats,
                section=table.section,
                state=current_state,
            )
        )

    return TableListOut(
        branch=branch,
        free=sum(
            item.state == TableState.FREE
            for item in results
        ),
        tables=results,
    )


@router.get(
    "/branches/{branch}/tables/{no}",
    response_model=TableOut,
)
def get_table(
    branch: str,
    no: str,
    db: Session = Depends(get_db),
) -> TableOut:
    if branch != "Baner":
        raise NoSuchBranch(branch)

    table = db.scalar(
        select(Table).where(
            Table.branch == branch,
            Table.no == no,
        )
    )

    if table is None:
        raise NoSuchTable(no)

    return TableOut(
        no=table.no,
        seats=table.seats,
        section=table.section,
        state=derive_state(table),
    )
