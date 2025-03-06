from pydantic import BaseModel
from typing import Optional
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class ShowBlog(BaseModel):
    title: str
    class Config():
        # orm_mode = True
        from_attributes=True

