import datetime
from typing import Generic, Optional, Sequence

from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            declarative_mixin, declared_attr, mapped_column)

from iqware.database.core import resolve_tablename
from iqware.database.types import Datetime, ModelReadT


def utc_now() -> Datetime:
    return datetime.datetime.now(datetime.UTC)


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return resolve_tablename(cls.__name__)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


@declarative_mixin
class TimestampMixin:
    created_date: Mapped[Datetime] = mapped_column(
        server_default=func.now(), nullable=True)
    updated_date: Mapped[Datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())


class BaseTimestamp(BaseModel):
    created_date: Datetime
    updated_date: Datetime


class TimestampUpdate(BaseModel):
    update_date: Optional[Datetime] = Field(default_factory=utc_now)


class PaginatedResponse(BaseModel, Generic[ModelReadT]):
    page: int
    total_pages: int
    count: int
    content: Sequence[ModelReadT]
