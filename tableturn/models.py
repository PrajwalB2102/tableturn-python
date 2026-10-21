
"""Dining tables. State is derived at read time."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    no: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    branch: Mapped[str] = mapped_column(
        String, default="Baner", nullable=False
    )
    seats: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    section: Mapped[str] = mapped_column(
        String, nullable=False
    )
