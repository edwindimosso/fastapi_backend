from time import time
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import get_db, engine
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .routers import post, user



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Database connection 
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapiDB",
            user="postgres",
            password="Admin123",
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("<<<<<<<<<<<< Database connection was successful! >>>>>>>>>>>>")
        break

    except Exception as error:
        print("Connection to database failed") 
        print("Error:", error)
        time.sleep(3)

@app.get("/")
def main():
    return "Hello, World!"


# ===================== POSTS =====================
app.include_router(post.router)

# ===================== USERS =====================
app.include_router(user.router)
