from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.book import Book

class BorrowedBookBase(SQLModel):
    borrowing_time: datetime
    return_status: str

class BorrowedBook(BorrowedBookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="borrowed_books")

    book_id: int = Field(foreign_key="book.id")

    book: Optional["Book"] = Relationship(back_populates="borrowed_books")

class BorrowedBookCreate(BorrowedBookBase):
    user_id: int
    book_id: int

class BorrowedBookUpdate(SQLModel):
    borrowing_time: Optional[datetime] = None
    return_status: Optional[str] = None
    user_id: Optional[int] = None
    book_id: Optional[int] = None

class BorrowedBookRead(BorrowedBookBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    book_id: int

    class Config:
        orm_mode = True
