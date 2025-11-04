from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from typing import Optional,List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import app.models as models
from . import schemas,utils
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/post",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts


@app.post("/posts", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
# def create_posts(post: Post):
    # cursor.execute(
    #     """ INSERT INTO posts(title,content,published)  VALUES(%s,%s,%s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.dict()) #or models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@app.get("/post/{id}",response_model=schemas.Post)
def get_post(id: int,db: Session=Depends(get_db)):
    # cursor.execute(""" select * from posts where id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id== id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} was not found",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING  * """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Posts of id:{id} is not present in the database",
        )
    post.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return post


@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, postt: schemas.PostCreate,db:Session = Depends(get_db)):
    # cursor.execute(
    #     """ UPDATE posts SET title  = %s, content= %s,published= %s WHERE id=%s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )
    post_query.update(postt.dict(),synchronize_session=False)
    db.commit()
    # post_query.update('title':'hey this is my update title')
    return post_query.first()

@app.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.Users,db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_users=models.User(**user.dict())
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    return new_users

@app.get("/user/{id}",response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == id).first()
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id:{id} does not exist")
    return user