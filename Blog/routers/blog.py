from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(tags=["blogs"])

get_db = database.get_db

@router.get("/blog" ,response_model=list[schemas.ShowBlog])
def showAllBlogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post("/blog",status_code=status.HTTP_201_CREATED )
def createBlog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT )
def destroy(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog:
        db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False )
        db.commit()
        return {"data": f"Blog with id {id} deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exit in db")


@router.put('/blog/{id}',status_code = status.HTTP_202_ACCEPTED )
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).update(request)
    db.commit()
    return {"data": f"Blog with id {id} updated"}
