from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from .. repository import user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
    )

get_db = database.get_db


@router.post('/',status_code=status.HTTP_201_CREATED)
def createUser(request: schemas.User, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.createUser(request,db)

@router.get('/',response_model=list[schemas.ShowUserForBlog])
def showAllUsers(db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.showAllUsers(db)

@router.get("/{user_id:int}",response_model=schemas.ShowUserForBlog)
def showUser(user_id:int, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.showUser(user_id,db)

@router.delete('/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
def destroyUser(user_id:int, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.destroyUser(user_id,db)