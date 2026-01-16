import math
from typing import Generic, Optional, Sequence, Type

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from iqware.database.models import PaginatedResponse
from iqware.database.types import Filters, ModelT, ModelReadT, SelectT


class PaginatorService(Generic[ModelT, ModelReadT]):
    def __init__(
            self, model: Type[ModelT], model_read: Type[ModelReadT],
            per_page: int) -> None:

        if per_page <= 0:
            raise ValueError(
                "The amount of items per page must be bigger than 0")

        self.model = model
        self.model_read = model_read
        self.per_page = per_page

    def _apply_filters(self, stmt: SelectT,
                       filters: Optional[Filters] = None) -> SelectT:
        return stmt.where(*filters) if filters else stmt

    def _get_count(
            self,
            database: Session,
            filters: Optional[Filters] = None) -> int:
        stmt = self._apply_filters(
            select(func.count()).select_from(self.model), filters)

        return database.scalar(stmt) or 0

    def _get_items(
            self,
            database: Session,
            page_index: int,
            per_page: int,
            count: int,
            filters: Optional[Filters] = None,) -> Sequence[ModelT]:
        offset = (page_index - 1) * per_page

        if not (0 <= offset < count):
            raise ValueError("This page does not exist")

        stmt = self._apply_filters(
            select(self.model),
            filters
        ).offset(offset).limit(per_page)

        return database.scalars(stmt).all()

    def get_page(
            self,
            page_index: int,
            database: Session,
            filters: Optional[Filters] = None) -> PaginatedResponse[ModelReadT]:
        if page_index <= 0:
            raise ValueError("Page must be 1 or bigger")

        count = self._get_count(database, filters)
        total_pages = math.ceil(count / self.per_page)
        items = self._get_items(database, page_index,
                                self.per_page, count, filters)
        content = [
            self.model_read.model_validate(item)
            for item in items
        ]

        return PaginatedResponse(
            index=page_index,
            total_pages=total_pages,
            count=count,
            content=content
        )
