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
    DATABASE_URL if not os.getenv("TESTING") else DATABASE_TEST_URL,  # Використовуємо тестову БД, якщо TESTING = 1
    echo=True if os.getenv("ENVIRONMENT") == "development" else False
)


def create_db_and_tables():
    try:
        # Explicitly import models to ensure they're registered with SQLModel
        from app.models.book import Book
        from app.models.author import Author
        from app.models.borrowed_book import BorrowedBook
        from app.models.user import User
        # (імпортуй всі потрібні моделі)

        # Test database connection
        with engine.connect() as conn:
            logger.info("Database connection successful")

        # Drop existing tables (⚠️ Увага: видалить всі дані)
        logger.warning("Dropping all existing tables...")
        SQLModel.metadata.drop_all(engine)
        logger.info("All tables dropped successfully.")

        # Create new tables
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")

        # Verify tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info("Existing tables: %s", existing_tables)

        # Check for expected tables
        expected_tables = ["book", "author", "book_author_link", "borrowedbook", "user"]
        for table in expected_tables:
            if table not in existing_tables:
                logger.error(f"Table '{table}' was not created")
            else:
                logger.info(f"Table '{table}' exists")

    except Exception as e:
        logger.error("Error creating tables: %s", str(e))
        raise

def clear_db():
    try:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        logger.info("Database cleared and tables recreated successfully")
    except Exception as e:
        logger.error("Error clearing database: %s", str(e))
        raise

def get_session() -> Generator[Session, Session, None]:
    with Session(engine) as session:
        yield session