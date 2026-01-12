from tests.models import DummyCreate


def get_dummy_create(name: str) -> DummyCreate:
    return DummyCreate(name=name)
