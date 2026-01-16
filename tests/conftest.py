from typing import Generator, List

from pytest import fixture
from sqlalchemy.orm import Session

from iqware.database.core import session_manager
from iqware.database.models import Base
from tests.db import test_engine, SessionTesting
from tests.factory import get_dummy_create, get_dummy_create_batch
from tests.models import DummyCreate


@fixture(scope="function")
def db_session() -> Generator[Session]:
    Base.metadata.create_all(bind=test_engine)

    with session_manager(SessionTesting) as session:
        yield session

    Base.metadata.drop_all(bind=test_engine)


@fixture
def dummy_create() -> DummyCreate:
    return get_dummy_create(name="dummy_test")


@fixture
def dummy_create_batch() -> List[DummyCreate]:
    return get_dummy_create_batch(name="dummy_test", amount=20)
