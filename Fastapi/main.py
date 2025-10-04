from fastapi import FastAPI,Response,status
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    Title:str
    Content:str
    Publication:bool = True
    Rating: Optional[int] = None

my_posts = [{"title":"post1","content":"about post1","id":1},{"title":"post2","content":"about post2","id":2}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message":"Hello World"}


@app.get("/Post")
def get_posts():
    return {"data":my_posts}

@app.post("/posts")
def create_post(new_post:Post):
    my_posts.append(new_post.dict())
    return {"new_post":my_posts}

@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post = find_posts(id)
    if not post:
        response.status_code = 404
    return {"post_details":post}
