from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/posts", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(models.PostModel).all()


@router.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def add_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.PostModel(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)
    return existing_post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()