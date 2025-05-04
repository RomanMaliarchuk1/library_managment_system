from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.database import get_session
from app.models.borrowed_book import BorrowedBookCreate, BorrowedBookRead, BorrowedBookUpdate
from app.crud.borrowed_books import crud_borrowed_books
from app.models.user import User
from app.models.book import Book
from app.utils.exceptions import LibraryException

router = APIRouter()


@router.post("/", response_model=BorrowedBookRead, status_code=status.HTTP_201_CREATED)
def borrow_book(
    *,
    db: Session = Depends(get_session),
    borrowed_book: BorrowedBookCreate
):
    try:
        borrowed_book = crud_borrowed_books.create(db=db, obj_in=borrowed_book)
        return borrowed_book
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Return a book (update borrowed book status)
@router.put("/{borrowed_book_id}", response_model=BorrowedBookRead)
def return_book(
    *,
    borrowed_book_id: int,
    db: Session = Depends(get_session),
    borrowed_book: BorrowedBookUpdate
):
    existing_borrowed_book = crud_borrowed_books.get(db=db, id=borrowed_book_id)
    if not existing_borrowed_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"BorrowedBook with ID {borrowed_book_id} not found"
        )

    try:
        updated_borrowed_book = crud_borrowed_books.update(db=db, db_obj=existing_borrowed_book, obj_in=borrowed_book)
        return updated_borrowed_book
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/user/{user_id}", response_model=List[BorrowedBookRead])
def get_borrowed_books_by_user(
    *,
    user_id: int,
    db: Session = Depends(get_session)
):
    try:
        borrowed_books = crud_borrowed_books.get_by_user(db=db, user_id=user_id)
        return borrowed_books
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/book/{book_id}", response_model=List[BorrowedBookRead])
def get_borrowed_books_by_book(
    *,
    book_id: int,
    db: Session = Depends(get_session)
):
    try:
        borrowed_books = crud_borrowed_books.get_by_book(db=db, book_id=book_id)
        return borrowed_books
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@router.delete("/{borrowed_book_id}", response_model=BorrowedBookRead)
def delete_borrowed_book(
    *,
    borrowed_book_id: int,
    db: Session = Depends(get_session)
):
    existing_borrowed_book = crud_borrowed_books.get(db=db, id=borrowed_book_id)
    if not existing_borrowed_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"BorrowedBook with ID {borrowed_book_id} not found"
        )

    try:
        deleted_borrowed_book = crud_borrowed_books.delete(db=db, db_obj=existing_borrowed_book)
        return deleted_borrowed_book
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get most popular books
@router.get("/most-popular-books", response_model=List[dict])
def get_most_popular_books(
    *,
    db: Session = Depends(get_session),
    top_n: int = 10
):
    try:
        popular_books = crud_borrowed_books.get_most_popular_books(db=db, top_n=top_n)
        return popular_books
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Get most popular authors
@router.get("/most-popular-authors", response_model=List[dict])
def get_most_popular_authors(
    *,
    db: Session = Depends(get_session),
    top_n: int = 10
):
    try:
        popular_authors = crud_borrowed_books.get_most_popular_authors(db=db, top_n=top_n)
        return popular_authors
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Get most popular categories
@router.get("/most-popular-categories", response_model=List[dict])
def get_most_popular_categories(
    *,
    db: Session = Depends(get_session),
    top_n: int = 10
):
    try:
        popular_categories = crud_borrowed_books.get_most_popular_categories(db=db, top_n=top_n)
        return popular_categories
    except LibraryException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))