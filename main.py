from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]



@app.get("/")
def index():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "Hello, About!"}

@app.get('/blog')
def show(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from the database'}
    else:
        return {'data': f'{limit} unpublished blogs from the database'}
    

@app.post('/blog')
def createBlog(request : Blog):                 
    return {'data': f'This blog is created with title as {request.title}'}

@app.get("/blog/{id:int}")
def show(id:int):
    return {"data":"Hello roll: "+str(id)}

@app.get("/blog/{id:int}/comments")
def show_comments(id:int, limit:int = 2):
    return {"data":{id,id+1}}

@app.get('/blog/unpublished')
def unpublished():
    return {"data":'All unpublished blogs'}

#uvicorn main:app --reload


