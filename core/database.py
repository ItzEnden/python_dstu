from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import settings


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
