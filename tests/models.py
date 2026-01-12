from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped

from iqware.database.models import Base, BaseTimestamp, TimestampMixin, TimestampUpdate
from pydantic import BaseModel


class Dummy(Base, TimestampMixin):
    name: Mapped[str]


class BaseDummy(BaseModel):
    name: str


class DummyCreate(BaseDummy):
    ...


class DummyRead(BaseTimestamp, BaseDummy):
    id: int


class DummyUpdate(TimestampUpdate, BaseModel):
    name: Optional[str] = None
