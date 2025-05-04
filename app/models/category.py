
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from app.models.book import BookCategoryLink


if TYPE_CHECKING:
    from app.models.book import Book


class CategoryBase(SQLModel):
    category_name: str
    description: Optional[str] = None


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    books: List["Book"] = Relationship(
        back_populates="categories",
        link_model=BookCategoryLink
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    category_name: Optional[str] = None
    description: Optional[str] = None


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True