from .secrets import password
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body,Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

#Creates Post Schema and defines data types
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# connect pg admin to python app
# "cursor_factory=RealDictCursor" this variable returns column name mapped with values
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres',
                                password=password, cursor_factory=RealDictCursor
                                )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Database connection failed!")
        print("Error: ", error)
        time.sleep(3)

# array of posts
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "fave films", "content": "Stalker & Solaris", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


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

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was does not exist")

    my_posts.pop(index)


    return {'message': f"post with id {id} was succesfully deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was does not exist")

    #logic for returning updated info
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

