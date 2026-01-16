from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if user.email:
        email_exists = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = utils.hash_password(user.password)

    new_user = models.UserModel(
        **user.dict(exclude={"password"}),
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.UserModel).all()


@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.UserModel).filter(models.UserModel.id == id)
    existing_user = user_query.first()

    if user.email:
        email_exists = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already exists")

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    

    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = utils.hash_password(user.password)

    user_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(existing_user)
    return existing_user



@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()