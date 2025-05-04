# app/models/books.py
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models.author import Author

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone


class BookAuthorLink(SQLModel, table=True):
    __tablename__ = "book_author_link"

    book_id: Optional[int] = Field(
        default=None, foreign_key="book.id", primary_key=True
    )
    author_id: Optional[int] = Field(
        default=None, foreign_key="author.id", primary_key=True
    )


class BookCategoryLink(SQLModel, table=True):
    __tablename__ = "book_category_link"

    book_id: Optional[int] = Field(
        default=None, foreign_key="book.id", primary_key=True
    )
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", primary_key=True
    )
    pass


class BookBase(SQLModel):
    title: str = Field(index=True)
    publication_year: int = Field(default=None)
    isbn: str = Field(unique=True, index=True)
    quantity: int = Field(default=1)


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    authors: List["Author"] = Relationship(
        back_populates="books",
        link_model=BookAuthorLink
    )

    categories: List["Category"] = Relationship(
        back_populates="books",
        link_model=BookCategoryLink
    )

    borrowed_books: List["BorrowedBook"] = Relationship(back_populates="book")


class BookCreate(BookBase):
    author_ids: List[int] = []
    category_ids: List[int] = []


class BookUpdate(SQLModel):
    title: Optional[str] = None
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: Optional[int] = None
    author_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None


class BookRead(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True