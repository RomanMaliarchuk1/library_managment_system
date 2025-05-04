from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.database import get_session
from app.models.user import UserRead, UserCreate, UserUpdate
from app.crud.users import crud_users

router = APIRouter()



@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_session)
):
    return crud_users.create(db=db, obj_in=user)

@router.get("/", response_model=List[UserRead])
def read_users(
        db: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 100
):
    return crud_users.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
def read_user(
        user_id: int,
        db: Session = Depends(get_session)
):
    user = crud_users.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
        user_id: int,
        user: UserUpdate,
        db: Session = Depends(get_session)
):
    db_user = crud_users.get(db=db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return crud_users.update(db=db, db_obj=db_user, obj_in=user)

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(
        user_id: int,
        db: Session = Depends(get_session)
):
    user = crud_users.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return crud_users.remove(db=db, id=user_id)
