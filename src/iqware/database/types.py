import datetime
from typing import Sequence, TypeVar

from pydantic import BaseModel
from sqlalchemy import ColumnElement, Select
from sqlalchemy.orm import DeclarativeBase


ModelT = TypeVar("ModelT", bound=DeclarativeBase)

ModelCreateT = TypeVar("ModelCreateT", bound=BaseModel)

ModelUpdateT = TypeVar("ModelUpdateT", bound=BaseModel)

ModelReadT = TypeVar("ModelReadT", bound=BaseModel)

SelectT = TypeVar("SelectT", bound=Select)

type Filters = Sequence[ColumnElement[bool]]

type Datetime = datetime.datetime
