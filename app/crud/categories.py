from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime, timezone
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.models.book import BookCategoryLink
from app.crud.base import CRUDBase
from app.utils.exceptions import LibraryException


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        category = Category(
            category_name=obj_in.category_name,
            description=obj_in.description
        )

        db.add(category)
        db.flush()
        db.commit()
        db.refresh(category)
        return category

    def get(self, db: Session, id: int) -> Category:
        db_obj = db.get(Category, id)
        if not db_obj:
            return None
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Category]:
        statement = select(Category).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results

    def update(self, db: Session, *, db_obj: Category, obj_in: CategoryUpdate) -> Category:
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db_obj.updated_at = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> None:
        db_obj = db.get(Category, id)
        if not db_obj:
            raise LibraryException(f"Category with ID {id} not found")

        statement = select(BookCategoryLink).where(BookCategoryLink.category_id == id)
        links = db.exec(statement).all()
        for link in links:
            db.delete(link)

        db.flush()

        db.delete(db_obj)
        db.commit()


crud_categories = CRUDCategory(Category)