from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from typing import Optional,List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import schemas,utils,models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from .routers import post,user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="postgres",
#             user="postgres",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was succesfull  ")
#         break
#     except Exception as error:
#         print("connecting to database failed check your code")
#         print("Error:", error)
#         time.sleep(2)

my_posts = [
    {"title": "post1", "content": "about post1", "id": 1},
    {"title": "post2", "content": "about post2", "id": 2},
]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

app.include_router(post.router)
app.include_router(user.router)