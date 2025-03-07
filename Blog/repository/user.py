from .. import models, schemas
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. hashing import Hash
from ..database import get_db

def createUser(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def showAllUsers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

def showUser(user_id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found in the db")
    return user

def destroyUser(user_id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found in the db")
    
    user.delete(synchronize_session=False)
    db.commit()
    return {"data": f"User with id {user_id} has been deleted"}
