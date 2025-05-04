from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime

from app.models.user import User, UserCreate, UserUpdate
from app.crud.base import CRUDBase
from app.utils.exceptions import LibraryException


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        user = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email
        )

        db.add(user)
        db.flush()
        db.commit()
        db.refresh(user)
        return user

    def get(self, db: Session, id: int) -> User:
        db_obj = db.get(User, id)
        if not db_obj:
            return None
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        statement = select(User).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> None:
        db_obj = db.get(User, id)
        if not db_obj:
            raise LibraryException(f"User with ID {id} not found")

        db.delete(db_obj)
        db.commit()

crud_users = CRUDUser(User)
