from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# Ensure database tables are created
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog",status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id:int}",response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(get_db),response : Response = None):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog:
        db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False )
        db.commit()
        return {"data": f"Blog with id {id} deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exit in db")


@app.put('/blog/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).update(request)
    db.commit()
    return {"data": f"Blog with id {id} updated"}