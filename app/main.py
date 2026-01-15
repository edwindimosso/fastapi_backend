from . import models,schemas
from .database import SessionLocal, engine, get_db
from fastapi import FastAPI, Depends
from .models import PostModel
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#Database connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastapiDB', 
                                user='postgres', 
                                password='Admin123', 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("<<<<<<<<<<<<<<<< Database connection was successful!>>>>>>>>>>>>>>")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(3)

@app.get("/")
def main():
    return "Hello, World!"



@app.get("/posts", response_model=list[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)): 
    posts = db.query(models.PostModel).all()
    return posts

 # cursor.execute("SELECT * FROM posts")
# posts = cursor.fetchall()

@app.post("/posts", response_model=schemas.PostResponse)
def add_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.PostModel(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

#nikipata namna ya kuweka latest post ntaweka hapa

@app.get("/posts/{id}") 
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id == id).first()
    if post:
        return post
    return "Post not found"

###<<<<<<<< IGNORE >>>>>>
#    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
#    post = cursor.fetchone()
#    if post:
#        return post 
#    return ("Post not found")


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # 1. Query the database for the existing post
    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    updated_post = post_query.first()

    if not updated_post:
        return "Post not found"

    # 2. Convert the incoming Pydantic model to a dictionary
    # Use post.model_dump() if using Pydantic v2, or post.dict() for v1
    update_data = post.dict()

    # 3. Update the database model instance with the new values
    post_query.update(update_data, synchronize_session=False)

    # 4. Commit and refresh
    db.commit()
    db.refresh(updated_post)

    return updated_post

    #<<<<<<<<<<<<<< IGNORE >>>>>>>>>#
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post:
    #         return updated_post 
        
    # return "Post not found"

@app.delete("/posts/{id}")
def delete_posts(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.PostModel).filter(models.PostModel.id == id).first()
    if deleted_post:
        db.delete(deleted_post)
        db.commit()
        db.refresh(deleted_post)
        return deleted_post
    
    
    return "Post not found"
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post:
    #         return deleted_post
        
    # return "Post not found"

@app.post("/users", response_model=schemas.UserResponse)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user