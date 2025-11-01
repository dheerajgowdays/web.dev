from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import fastapi.models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was succesfull  ")
        break
    except Exception as error:
        print("connecting to database failed check your code")
        print("Error:", error)
        time.sleep(2)

my_posts = [
    {"title": "post1", "content": "about post1", "id": 1},
    {"title": "post2", "content": "about post2", "id": 2},
]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/post")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO posts(title,content,published)  VALUES(%s,%s,%s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute(""" select * from posts where id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} was not found",
        )
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING  * """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Posts of id:{id} is not present in the database",
        )
    conn.commit()
    return {"delete_post": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE posts SET title  = %s, content= %s,published= %s WHERE id=%s RETURNING * """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )
    return {"data": updated_post}/home/dheeraj/FastApi/__pycache__