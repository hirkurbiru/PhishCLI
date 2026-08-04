"""
PhishCLI - Database Connection Engine

Manages SQLite connection lifecycles, session creation,
and schema initialization.
"""

from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config.constants import DB_PATH
from config.logging_config import logger
from config.settings import settings
from utils.exceptions import DatabaseError

# ==========================================================
# SQLAlchemy Base Model
# ==========================================================

Base = declarative_base()

# ==========================================================
# Database Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
    future=True,
)

# ==========================================================
# SQLite Configuration
# ==========================================================

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Configure SQLite every time a new connection is created.
    """

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("PRAGMA journal_mode = WAL")

    cursor.close()


# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ==========================================================
# Table Creation
# ==========================================================

def create_tables() -> None:
    """
    Creates all registered SQLAlchemy tables.
    """
    Base.metadata.create_all(bind=engine)


# ==========================================================
# Database Initialization
# ==========================================================

def init_db() -> None:
    """
    Initializes the local database.
    """

    try:

        logger.info(f"Initializing database at: {DB_PATH}")

        create_tables()

        logger.info("Database initialized successfully.")

    except Exception as e:

        logger.critical(f"Failed to initialize database: {e}")

        raise DatabaseError(
            "Could not initialize database.",
            details=str(e),
        )


# ==========================================================
# Database Session
# ==========================================================

def get_db() -> Generator[Session, None, None]:
    """
    Creates a database session.

    Usage:

        for db in get_db():
            ...

    """

    db = SessionLocal()

    try:

        yield db

    except Exception as e:

        db.rollback()

        logger.error(f"Database session rolled back: {e}")

        raise DatabaseError(
            "Database operation failed.",
            details=str(e),
        )

    finally:

        db.close()