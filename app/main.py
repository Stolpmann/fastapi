from .secrets import password
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body,Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db

#Creates Tables in postgress
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#Connects to database through session object



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
    # Executes SQL query via cursor var
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

# HTTP POST REQUEST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Stages new post
    # Values use '%s' to prevent SQL injection attack
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    #pushes new post to sql database
    conn.commit()
    return {"data": new_post}

# use path parameter ({id}) to get url of specific post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} does not exist")


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts  SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, id,))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was does not exist")

    return {"data": updated_post}

