from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import os
from time import sleep

DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Create sync engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db(retries=5):
    # Try to connect a few times (useful when running with docker-compose)
    from sqlalchemy.exc import OperationalError
    attempt = 0
    while attempt < retries:
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            attempt += 1
            sleep(2)
    # last try without catching
    Base.metadata.create_all(bind=engine)
