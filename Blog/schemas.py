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
        from_attributes = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        from_attributes = True

class ShowUserForBlog(BaseModel):
    name:str
    email:str
    blogs:List[BlogBase]=[]
    class Config():
        from_attributes = True



class ShowBlog(BaseModel):
    title: str
    body:str
    creator: ShowUser

    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None