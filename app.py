from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing  import Text, Optional
from datetime import datetime
from uuid import uuid4 as uui

app = FastAPI()

posts = []

class Post(BaseModel):
    id: Optional[str]
    title:str
    author: str
    content: Text
    crated_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get("/")
def read_root():
    return {"Welcome":"Welcome to my API"}

@app.get("/post")
def get_post():
    return posts

@app.post("/posts")
def save_post(post: Post):
    post.id = str(uui())
    posts.append(post.dict())
    return posts[-1]


@app.get("/post/{post_id}")
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post Not Found")

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"]= updatedPost.dict()["title"]
            posts[index]["content"]= updatedPost.dict()["content"]
            posts[index]["author"]= updatedPost.dict()["author"]
            return {"message": "Post has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")