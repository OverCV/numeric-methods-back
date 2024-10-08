from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///database.db", echo=True, future=True)

SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def get_db() -> SessionLocal:
    db: sessionmaker = SessionLocal()
    try:
        yield db
    finally:
        db.close()
