from . import models
from .database import SessionLocal, engine, get_db
from fastapi import FastAPI, Depends
from app.models import Post
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



posts = [
    Post(id=1, title="First Post", content="This is the content of the first post"),
    Post(id=2, title="Second Post", content="This is the content of the second post"),
    Post(id=3, title="Third Post", content="This is the content of the third post"),
    Post(id=4, title="Fourth Post", content="This is the content of the fourth post"),
    Post(id=5, title="Fifth Post", content="This is the content of the fifth post")
]

#Database connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastapiDB', 
                                user='postgres', 
                                password='Admin123', 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("<<<<<<<<<<<<<<<<Database connection was successful!>>>>>>>>>>>>>>/n")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(3)

@app.get("/")
def main():
    return "Hello, World!"



@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)): 
    posts = db.query(models.PostModel).all()
    return posts 

 # cursor.execute("SELECT * FROM posts")
# posts = cursor.fetchall()

@app.post("/posts")
def add_posts(post: Post, db: Session = Depends(get_db)):
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


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.PostModel).filter(models.PostModel.id == id).first()
    if updated_post:
        updated_post.title = post.title
        updated_post.content = post.content
        db.commit()
        db.refresh(updated_post)
        return updated_post
    
    return "Post not found"


    #<<<<<<<<<<<<<< IGNORE >>>>>>>>>#
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post:
    #         return updated_post 
        
    # return "Post not found"

@app.delete("/posts/{id}")
def delete_posts(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post:
            return deleted_post
        
    return "Post not found"
