from .secrets import password
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body,Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post,user


#Creates Tables in postgress
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

#allows program to search post.py and user.py to check if any HTTP request match functions
app.include_router(post.router)
app.include_router(user.router)


# Path Operation
@app.get("/")
def root():
    return {"message": "Hello World"}

