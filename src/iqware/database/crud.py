from typing import Generic, Type

from sqlalchemy.orm import Session

from iqware.database.types import (
    ModelT, ModelCreateT, ModelUpdateT)


class CRUDService(Generic[ModelT, ModelCreateT, ModelUpdateT]):
    def __init__(self, model: Type[ModelT]) -> None:
        self.model = model

    def _prepare_data(
        self,
        model_in: ModelCreateT | ModelUpdateT,
        exclude_unset: bool
    ) -> dict:
        return model_in.model_dump(exclude_unset=exclude_unset)

    def create(self, model_in: ModelCreateT, database: Session) -> ModelT:
        data = self._prepare_data(model_in=model_in, exclude_unset=False)
        model = self.model(**data)
        database.add(model)
        database.commit()
        database.refresh(model)

        return model

    def read(self, id: int, database: Session) -> ModelT | None:
        return database.get(self.model, id)

    def update(
        self,
        db_obj: ModelT,
        obj_in: ModelUpdateT,
        database: Session
    ) -> ModelT:
        data = self._prepare_data(obj_in, exclude_unset=True)

        for field, value in data.items():
            setattr(db_obj, field, value)

        database.commit()
        database.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: ModelT, database: Session) -> None:
        database.delete(db_obj)
        database.commit()

        return None
