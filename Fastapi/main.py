from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    Title: str
    Content: str
    Publication: bool = True
    Rating: Optional[int] = None


my_posts = [
    {"title": "post1", "content": "about post1", "id": 1},
    {"title": "post2", "content": "about post2", "id": 2},
]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/Post")
def get_posts(new_post: dict = Body(...)):
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    my_posts.append(new_post.dict())
    return {"new_post": my_posts}


@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found ",
        )
    return {"post_details": post}


@app.delete("/post/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,detail=f"Post is {id} NOT THERE")
    my_posts.pop(index)
    return {"post_deleted": f"{id} post is deleted"}

@app.put("/post/{id}")
def update_post(id: int,post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,detail=f"Post is {id} NOT THERE")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message":"updated post"}
