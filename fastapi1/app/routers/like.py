from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm  import  Session
from typing import Optional,List
from .. import schemas,models,oauth2
from .. import database

router = APIRouter(
    prefix="/like",
    tags=["Likes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like,db: Session = Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Like).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {like.post_id} does not exist")

    like_query = db.query(models.Like).filter(
        models.Like.post_id == like.post_id,models.Like.user_id == current_user.id
        )
    found_like = like_query.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"users{current_user.id} has already liked the post{like.post_id}")
        new_like = models.Like(post_id = like.post_id,user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message":"successfully added like"}
    else:
        if not found_like:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Like doest exist")
        like_query.delete(Synchronize_session = False)
        db.commit()
        return {"message":"Successfully like deleted"}