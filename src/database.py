import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Find the root directory of the project.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load database settings from the .env file.
load_dotenv(BASE_DIR / ".env")


# Build the connection URL safely.
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST", "localhost"),
    port=int(os.getenv("PGPORT", "5432")),
    database=os.getenv("PGDATABASE"),
)


# Create the database engine.
engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


# Create database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# Base class for database models.
class Base(DeclarativeBase):
    pass
