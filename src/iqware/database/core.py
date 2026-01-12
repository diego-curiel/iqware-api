import re
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from iqware.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def resolve_tablename(name: str) -> str:
    names = re.split(r"(=?[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


@contextmanager
def session_manager(session_maker: sessionmaker) -> Generator[Session]:
    session: Session = session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session]:
    with session_manager(SessionLocal) as session:
        yield session
