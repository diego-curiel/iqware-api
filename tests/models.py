from typing import Optional
from sqlalchemy.orm import Mapped

from iqware.database.models import (
    Base, BaseTimestamp, PublicModel, TimestampMixin, TimestampUpdate)
from pydantic import BaseModel


class Dummy(Base, TimestampMixin):
    name: Mapped[str]


class BaseDummy(BaseModel):
    name: str


class DummyCreate(BaseDummy):
    ...


class DummyRead(PublicModel, BaseTimestamp, BaseDummy):
    ...


class DummyUpdate(TimestampUpdate, BaseModel):
    name: Optional[str] = None
