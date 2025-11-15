from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm  import  Session
from typing import Optional,List
from .. import schemas,models,oauth2
from .. import database

router = APIRouter(
    prefix="/like",
    tags="Likes"
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like,db: Session = Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):

    like_query = db.query(models.Like).filter(
        models.Like.post_id == like.post_id,models.Like.user_id == like.user_id
        )
    found_like = like_query.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"users{current_user.id} has already liked the post{like.post_id}")
        new_vote = models.Like(post_id = like.post_id,user_id = like.user_id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added like"}
    else:
        if not found_like:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Like doest exist")
        