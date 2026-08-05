import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:aziz1234@localhost:5432/erp")

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass