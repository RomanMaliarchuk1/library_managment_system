from sqlmodel import Session, select
from sqlalchemy import func
from datetime import datetime, timezone

from app.models.borrowed_book import BorrowedBook, BorrowedBookCreate, BorrowedBookUpdate
from app.models.user import User
from app.models.author import Author
from app.models.category import Category
from app.models.book import Book
from app.utils.exceptions import LibraryException


class CRUDBorrowedBook:
    def create(self, db: Session, *, obj_in: BorrowedBookCreate) -> BorrowedBook:
        user = db.get(User, obj_in.user_id)
        if not user:
            raise LibraryException(f"User with ID {obj_in.user_id} not found.")

        book = db.get(Book, obj_in.book_id)
        if not book:
            raise LibraryException(f"Book with ID {obj_in.book_id} not found.")

        borrowed_book = BorrowedBook(
            user_id=obj_in.user_id,
            book_id=obj_in.book_id,
            borrowing_time=obj_in.borrowing_time,
            return_status=obj_in.return_status
        )

        db.add(borrowed_book)
        db.commit()
        db.refresh(borrowed_book)

        return borrowed_book

    def get(self, db: Session, id: int) -> BorrowedBook:
        borrowed_book = db.get(BorrowedBook, id)
        if not borrowed_book:
            return None
        return borrowed_book

    def get_by_user(self, db: Session, user_id: int) -> list[BorrowedBook]:
        borrowed_books = db.exec(select(BorrowedBook).where(BorrowedBook.user_id == user_id)).all()
        if not borrowed_books:
            return None
        return borrowed_books

    def get_by_book(self, db: Session, book_id: int) -> list[BorrowedBook]:
        borrowed_books = db.exec(select(BorrowedBook).where(BorrowedBook.book_id == book_id)).all()
        if not borrowed_books:
            return None
        return borrowed_books

    def update(self, db: Session, *, db_obj: BorrowedBook, obj_in: BorrowedBookUpdate) -> BorrowedBook:
        update_data = obj_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db_obj.updated_at = datetime.now(timezone.utc)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def delete(self, db: Session, *, db_obj: BorrowedBook) -> BorrowedBook:
        db.delete(db_obj)
        db.commit()
        return db_obj

    def get_most_popular_books(self, db: Session, top_n: int = 10) -> list[Book]:
        result = db.exec(
            select(
                Book,
                func.count(BorrowedBook.book_id).label("borrow_count")
            )
            .join(BorrowedBook, BorrowedBook.book_id == Book.id)
            .group_by(Book.id)
            .order_by(func.count(BorrowedBook.book_id).desc())
            .limit(top_n)
        ).all()

        if not result:
            raise LibraryException("No borrowed books found for statistics.")

        # Return the most borrowed books
        return [{"book": book, "borrow_count": borrow_count} for book, borrow_count in result]

    # Get most popular authors (authors with the most borrowed books)
    def get_most_popular_authors(self, db: Session, top_n: int = 10) -> list[Author]:
        result = db.exec(
            select(
                Author,
                func.count(BorrowedBook.book_id).label("borrow_count")
            )
            .join(Book, Book.author_id == Author.id)
            .join(BorrowedBook, BorrowedBook.book_id == Book.id)
            .group_by(Author.id)
            .order_by(func.count(BorrowedBook.book_id).desc())
            .limit(top_n)
        ).all()

        if not result:
            raise LibraryException("No borrowed books found for statistics.")

        # Return the most popular authors
        return [{"author": author, "borrow_count": borrow_count} for author, borrow_count in result]

    # Get most popular categories (categories with the most borrowed books)
    def get_most_popular_categories(self, db: Session, top_n: int = 10) -> list[Category]:
        result = db.exec(
            select(
                Category,
                func.count(BorrowedBook.book_id).label("borrow_count")
            )
            .join(Book, Book.category_id == Category.id)
            .join(BorrowedBook, BorrowedBook.book_id == Book.id)
            .group_by(Category.id)
            .order_by(func.count(BorrowedBook.book_id).desc())
            .limit(top_n)
        ).all()

        if not result:
            raise LibraryException("No borrowed books found for statistics.")

        # Return the most popular categories
        return [{"category": category, "borrow_count": borrow_count} for category, borrow_count in result]


crud_borrowed_books = CRUDBorrowedBook()
