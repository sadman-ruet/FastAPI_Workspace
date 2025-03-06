from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import hash

app = FastAPI()

# Ensure database tables are created
models.Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog",status_code=201,tags=["blogs"])
def createBlog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog",tags=["blogs"],response_model=list[schemas.ShowBlog])
def showAllBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id:int}",response_model=schemas.ShowBlog,tags=["blogs"])
def showBlog(id, db: Session = Depends(get_db),response : Response = None):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT,tags=["blogs"])
def destroy(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog:
        db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False )
        db.commit()
        return {"data": f"Blog with id {id} deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exit in db")


@app.put('/blog/{id}',status_code = status.HTTP_202_ACCEPTED,tags=["blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).update(request)
    db.commit()
    return {"data": f"Blog with id {id} updated"}


@app.post('/user',status_code=status.HTTP_201_CREATED,tags=["users"])
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user',tags=["users"],response_model=list[schemas.ShowUserForBlog])
def showAllUsers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/user/{user_id:int}",response_model=schemas.ShowUserForBlog,tags=["users"])
def showUser(user_id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found in the db")
    return user

@app.delete('/user/{user_id}',status_code=status.HTTP_204_NO_CONTENT,tags=["users"])
def destroyUser(user_id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found in the db")
    
    user.delete(synchronize_session=False)
    db.commit()
    return {"data": f"User with id {user_id} has been deleted"}