from pydantic import BaseModel
from typing import Optional, List
from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    user_id: int
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True

class ShowUserForBlog(BaseModel):
    name:str
    email:str
    blogs:List[BlogBase]=[]
    class Config():
        orm_mode = True



class ShowBlog(BaseModel):
    title: str
    body:str
    creator: ShowUser

    class Config():
        orm_mode = True