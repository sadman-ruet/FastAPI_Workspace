from .. import database, models, schemas
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
get_db = database.get_db

def showAllBlogs(db:Session = Depends(database.get_db)):
    return db.query(models.Blog).all()

def createBlog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroyBlog(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog:
        db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False )
        db.commit()
        return {"data": f"Blog with id {id} deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exit in db")
    
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).update(request)
    db.commit()
    return {"data": f"Blog with id {id} updated"}