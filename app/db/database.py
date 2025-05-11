from typing import Generator
from sqlmodel import SQLModel, create_engine, Session, inspect
from app.config import get_settings
from app.utils.logger import setup_logging
import os

settings = get_settings()
logger = setup_logging(log_level_str=settings.LOG_LEVEL if hasattr(settings, "LOG_LEVEL") else "INFO")

logger.info("DATABASE_URL: %s", settings.DATABASE_URL)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/library")
DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL", "postgresql://postgres:postgres@localhost:5432/library_test")

engine = create_engine(
    DATABASE_URL if not os.getenv("TESTING") else DATABASE_TEST_URL,
    echo=True if os.getenv("ENVIRONMENT") == "development" else False
)


def get_session() -> Generator[Session, Session, None]:
    with Session(engine) as session:
        yield session