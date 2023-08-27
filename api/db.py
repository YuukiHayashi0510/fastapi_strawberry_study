from typing import Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "postgresql://postgres:postgres@postgres:5432/postgres_db", echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


def get_db():
    "@deprecated: 今は使ってない"
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


class SessionService:
    def __init__(self):
        self.session = SessionLocal()
        print(f'{"="*25}session{"="*25}', flush=True)

    def __del__(self):
        self.session.close()

    def save(self, data: Any):
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
