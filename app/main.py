from . import models, schemas, utils
from .database import get_db, engine
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def main():
    return "Hello, World!"


# ===================== POSTS =====================

@app.get("/posts", response_model=list[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(models.PostModel).all()


@app.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def add_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.PostModel(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)
    return existing_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()


# ===================== USERS =====================

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
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




@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.UserModel).all()


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.put("/users/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.UserModel).filter(models.UserModel.id == id)
    existing_user = user_query.first()



    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    

    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = utils.hash_password(user.password)

    user_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(existing_user)
    return existing_user



@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()