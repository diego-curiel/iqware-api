from iqware.database.crud import CRUDService
from sqlalchemy.orm import Session
from tests.models import Dummy, DummyCreate, DummyUpdate


class DummyCRUD(CRUDService[Dummy, DummyCreate, DummyUpdate]):
    pass


def test_crud_create(db_session: Session, dummy_create: DummyCreate) -> None:
    crud_service = DummyCRUD(model=Dummy)
    dummy = crud_service.create(dummy_create, db_session)

    assert dummy.id, "The object does not have a primary key (id)"
    assert dummy.name == dummy_create.name, "The object name has changed"


def test_crud_read(db_session: Session, dummy_create: DummyCreate) -> None:
    crud_service = DummyCRUD(model=Dummy)
    dummy = crud_service.create(dummy_create, db_session)
    db_dummy = crud_service.read(dummy.id, db_session)

    assert db_dummy is not None, "Got an empty object from the database"
    assert db_dummy is dummy, "The object retrieved from the database is different"


def test_crud_read_empty(db_session: Session) -> None:
    crud_service = DummyCRUD(model=Dummy)
    db_dummy = crud_service.read(1, db_session)

    assert db_dummy is None, "Got a response from the database"


def test_crud_update(db_session: Session, dummy_create: DummyCreate) -> None:
    crud_service = DummyCRUD(model=Dummy)
    dummy = crud_service.create(dummy_create, db_session)
    dummy_update = DummyUpdate(name=f"{dummy_create.name}123")
    db_dummy = crud_service.update(dummy, dummy_update, db_session)

    assert dummy is db_dummy, "The object was detached from the database"
    assert db_dummy.name == dummy_update.name, "The object was not updated"


def test_crud_delete(db_session: Session, dummy_create: DummyCreate) -> None:
    crud_service = DummyCRUD(model=Dummy)
    dummy = crud_service.create(dummy_create, db_session)
    db_dummy = crud_service.delete(dummy, db_session)

    assert db_dummy is None, "The object was not deleted successfully"
