from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body,Optional
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#Creates Post Schema and defines data types
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# array of posts
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "fave films", "content": "Stalker & Solaris", "id": 2}]


# Path Operation
@app.get("/")
def root():
    return {"message": "Hello World"}

#HTTP GET REQUEST
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# HTTP POST REQUEST
@app.post("/posts", status_code=status.HTTP_201_CREATED)

#Creates Function that takes pydantic model validates data and assigns it into a variable
def create_post(post: Post):
    # Convert Pydantic model into Dictionary
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    # Append post to dictionary of posts
    my_posts.append(post_dict)
    return {"data": post_dict }

# use path parameter ({id}) to get url of specific post
@app.get("/posts/{id}")

def get_post(id):
    print(id)
    return {"post_detail": f"here is Post {id}"}