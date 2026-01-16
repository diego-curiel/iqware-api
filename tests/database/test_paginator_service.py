from typing import List, Sequence

from sqlalchemy.orm import Session

from iqware import database
from iqware.database.models import PaginatedResponse
from iqware.database.paginator import PaginatorService
from tests.factory import create_dummies
from tests.models import Dummy, DummyCreate, DummyRead


class DummyPaginator(PaginatorService[Dummy, DummyRead]):
    ...


def assert_valid_content(page_content: Sequence[DummyRead],
                         expected_content: List[Dummy]) -> None:
    assert all([
        page_dummy.name == expect_dummy.name
        for page_dummy, expect_dummy in zip(page_content, expected_content)
    ]), "The response content does not match with the expected content"


def assert_valid_page(
        page: PaginatedResponse,
        expected_index: int,
        expected_total_pages: int,
        expected_content: List[Dummy]) -> None:
    assert isinstance(page, PaginatedResponse)
    assert page.index == expected_index
    assert page.total_pages == expected_total_pages
    assert_valid_content(page.content, expected_content)


def test_get_page(
        db_session: Session,
        dummy_create_batch: List[DummyCreate]) -> None:
    paginator = DummyPaginator(model=Dummy, model_read=DummyRead, per_page=20)
    dummies = create_dummies(db_session, dummy_create_batch)
    page = paginator.get_page(
        page_index=1,
        database=db_session
    )
    assert_valid_page(page, expected_index=1, expected_total_pages=1,
                      expected_content=dummies)


def test_pagination_even(
        db_session: Session,
        dummy_create_batch: List[DummyCreate]) -> None:
    slice_pos = 10
    paginator = DummyPaginator(
        model=Dummy, model_read=DummyRead, per_page=slice_pos)
    dummies = create_dummies(db_session, dummy_create_batch)
    page_1 = paginator.get_page(
        page_index=1,
        database=db_session)
    page_2 = paginator.get_page(
        page_index=2,
        database=db_session
    )
    assert_valid_page(page_1, expected_index=1, expected_total_pages=2,
                      expected_content=dummies[:slice_pos])
    assert_valid_page(page_2, expected_index=2, expected_total_pages=2,
                      expected_content=dummies[slice_pos:])


def test_pagination_uneven(
        db_session: Session,
        dummy_create_batch: List[DummyCreate]) -> None:
    slice_pos = 8
    paginator = DummyPaginator(
        model=Dummy, model_read=DummyRead, per_page=slice_pos)
    dummies = create_dummies(db_session, dummy_create_batch)
    page_1 = paginator.get_page(
        page_index=1,
        database=db_session
    )
    page_2 = paginator.get_page(
        page_index=2,
        database=db_session
    )
    page_3 = paginator.get_page(
        page_index=3,
        database=db_session
    )
    assert_valid_page(page_1, expected_index=1, expected_total_pages=3,
                      expected_content=dummies[:slice_pos])
    assert_valid_page(page_2, expected_index=2, expected_total_pages=3,
                      expected_content=dummies[slice_pos:slice_pos*2])
    assert_valid_page(page_3, expected_index=3, expected_total_pages=3,
                      expected_content=dummies[slice_pos*2:slice_pos*3])


def test_pagination_filter(db_session: Session,
                           dummy_create_batch: List[DummyCreate]) -> None:
    paginator = DummyPaginator(model=Dummy, model_read=DummyRead, per_page=20)
    dummies = create_dummies(db_session, dummy_create_batch)
    page = paginator.get_page(
        page_index=1,
        database=db_session,
        filters=[Dummy.name.ilike("%test_11")]
    )

    assert_valid_page(
        page=page,
        expected_index=1,
        expected_total_pages=1,
        expected_content=dummies[11:12]
    )
