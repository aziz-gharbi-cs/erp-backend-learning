from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:aziz1234@localhost:5432/erp"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass