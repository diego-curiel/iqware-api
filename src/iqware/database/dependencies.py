from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from iqware.database.core import get_db


type DatabaseDep = Annotated[Session, Depends(get_db)]
