# app/api/books.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from app.db.database import get_session
from app.models.book import BookCreate, BookRead, BookUpdate
from app.crud.books import crud_books
# from app.services.book_service import BookService

router = APIRouter()
# book_service = BookService()


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_session)
):
    # Check if a book with the same ISBN already exists
    existing_books = crud_books.search_books(db, title=None, author_id=None)
    for existing_book in existing_books:
        if existing_book.isbn == book.isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ISBN {book.isbn} already exists"
            )

    return crud_books.create_with_relations(db=db, obj_in=book)


@router.get("/", response_model=List[BookRead])
def read_books(
        *,
        db: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100,
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None
):
    return crud_books.search_books(
        db=db,
        title=title,
        author_id=author_id,
        category_id=category_id,
        skip=skip,
        limit=limit
    )


@router.get("/{book_id}", response_model=BookRead)
def read_book(
        *,
        book_id: int,
        db: Session = Depends(get_session)
):
    book = crud_books.get(db=db, id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book


@router.put("/{book_id}", response_model=BookRead)
def update_book(
        *,
        book_id: int,
        book: BookUpdate,
        db: Session = Depends(get_session)
):
    db_book = crud_books.get(db=db, id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    # Check ISBN uniqueness if it's being updated
    if book.isbn and book.isbn != db_book.isbn:
        existing_books = crud_books.search_books(db, title=None, author_id=None, category_id=None)
        for existing_book in existing_books:
            if existing_book.isbn == book.isbn:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book with ISBN {book.isbn} already exists"
                )

    return crud_books.update_with_relations(db=db, db_obj=db_book, obj_in=book)


@router.delete("/{book_id}", response_model=BookRead)
def delete_book(
        *,
        book_id: int,
        db: Session = Depends(get_session)
):
    book = crud_books.get(db=db, id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    crud_books.remove(db=db, id=book_id)

    deleted_book = crud_books.get(db=db, id=book_id)
    if deleted_book:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete the book with ID {book_id}"
        )

    return book

@router.get("/search/", response_model=List[BookRead])
def search_books(
        *,
        db: Session = Depends(get_session),
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None
):
    return crud_books.search_books(
        db=db,
        title=title,
        author_id=author_id,
        category_id=category_id
    )
