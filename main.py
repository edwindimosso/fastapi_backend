from fastapi import FastAPI
from models import Post
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
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
        print("<<<<<<<<<<<<<<<<Database connection was successful!>>>>>>>>>>>>>>")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(3)

@app.get("/")
def main():
    return "Hello, World!"

@app.get("/posts")
def get_all_posts():
    return posts

@app.post("/posts")
def add_posts(post: Post):
    post.id = randrange(1000000)
    posts.append(post)
    return post

@app.get("/posts/latest")
def get_latest_post():
    return posts[-1]  # leta post ya mwisho 

@app.get("/posts/{id}")
def get_post(id: int):
    for post in posts:
        if post.id == id:
            return post
        
    return ("Post not found")

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for i in range(len(posts)):
        if posts[i].id == id:
            posts[i] = post
            return post
        
    return "Post not found"

@app.delete("/posts/{id}")
def delete_posts(id: int):
    for i in range(len(posts)):
        if posts[i].id == id:
            deleted_post = posts.pop(i)
            return deleted_post
        
    return "Post not found"
