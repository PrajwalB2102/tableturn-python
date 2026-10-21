"""Request and response models. Every response goes through one of these.
Optional fields are left out of the answer when they have no value (the routes serialise with exclude_none), so a free
table carries no party and a waiting party no table."""

from enum import Enum

from pydantic import BaseModel, ConfigDict


class Section(str, Enum):
    WINDOW = "Window"
    GARDEN = "Garden"
    INDOOR = "Indoor"


class TableState(str, Enum):
    FREE = "free"
    SEATED = "seated"
    UNCLEARED = "uncleared"


class TableOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    no: str
    seats: int
    section: Section
    state: TableState
    party_id: str | None = None
    seated_minutes: int | None = None


class TableListOut(BaseModel):
    branch: str
    free: int
    tables: list[TableOut]
