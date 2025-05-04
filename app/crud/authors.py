from typing import List, Optional
from sqlmodel import Session, select

from app.utils.exceptions import LibraryException
from app.models.author import Author, AuthorCreate, AuthorUpdate
from app.models.book import BookAuthorLink
from app.crud.base import CRUDBase
from datetime import datetime, timezone


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def create(self, db: Session, *, obj_in: AuthorCreate) -> Author:

        author = Author(
        first_name = obj_in.first_name,
        second_name = obj_in.second_name,
        biography = obj_in.biography,
        )

        db.add(author)
        db.flush()

        db.commit()
        db.refresh(author)

        return author

    def get(self, db: Session, id: int) -> Author:
        db_obj = db.get(Author, id)
        if not db_obj:
            return None
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Author]:
        statement = select(Author).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results

    def update(self, db, *, db_obj, obj_in):
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db_obj.updated_at = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def delete(self, db: Session, *, id: int) -> None:
        db_obj = db.get(Author, id)
        if not db_obj:
            raise LibraryException(f"Author with ID {id} not found")

        statement = select(BookAuthorLink).where(BookAuthorLink.author_id == id)
        links = db.exec(statement).all()
        for link in links:
            db.delete(link)

        db.flush()

        db.delete(db_obj)
        db.commit()

crud_authors = CRUDAuthor(Author)