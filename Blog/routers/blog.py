from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    tags=["blogs"],
    prefix="/blog"
    )

get_db = database.get_db

@router.get("/" ,response_model=list[schemas.ShowBlog])
def showAllBlogs(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.showAllBlogs(db)

@router.post("/",status_code=status.HTTP_201_CREATED )
def createBlog(request: schemas.Blog, db: Session = Depends(database.get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.createBlog(request, db)


@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def destroyBlog(id,db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroyBlog(id,db)


@router.put('/{id}',status_code = status.HTTP_202_ACCEPTED )
def update(id, request: schemas.Blog, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id,schemas.Blog,db)
