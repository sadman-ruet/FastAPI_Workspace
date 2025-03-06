from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session
from .. hashing import hash

router = APIRouter(tags=["Users"])

get_db = database.get_db


@router.post('/user',status_code=status.HTTP_201_CREATED)
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user',response_model=list[schemas.ShowUserForBlog])
def showAllUsers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/user/{user_id:int}",response_model=schemas.ShowUserForBlog)
def showUser(user_id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found in the db")
    return user

@router.delete('/user/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
def destroyUser(user_id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found in the db")
    
    user.delete(synchronize_session=False)
    db.commit()
    return {"data": f"User with id {user_id} has been deleted"}