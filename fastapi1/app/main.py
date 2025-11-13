from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from app.database import engine
from .routers import post,user,auth
from .config import settings


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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)