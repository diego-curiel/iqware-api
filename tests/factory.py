from typing import List

from sqlalchemy.orm import Session

from tests.models import Dummy, DummyCreate


def get_dummy_create(name: str) -> DummyCreate:
    return DummyCreate(name=name)


def get_dummy_create_batch(name: str, amount: int) -> List[DummyCreate]:
    return [
        DummyCreate(name=f"{name}_{index}")
        for index in range(amount)
    ]


def create_dummies(
        db_session: Session,
        dummy_create_batch: List[DummyCreate]) -> List[Dummy]:
    dummies = [
        Dummy(**dummy_create.model_dump(exclude_unset=True))
        for dummy_create in dummy_create_batch
    ]
    db_session.add_all(dummies)
    db_session.commit()

    return dummies
