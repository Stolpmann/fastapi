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
from . import models, schemas
from .database import engine, SessionLocal, get_db

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


# Path Operation
@app.get("/")
def root():
    return {"message": "Hello World"}


#HTTP GET REQUEST
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    ## Executes SQL query via cursor var
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# HTTP POST REQUEST
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    ## Stages new post
    ## Values use '%s' to prevent SQL injection attack
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    ## pushes new post to sql database
    # conn.commit()

    ## This code
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    ## gets replaced by
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# use path parameter ({id}) to get url of specific post
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    ## returns
    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} does not exist")

    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts  SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id,))
    # updated_post = cursor.fetchone()
    # conn.commit()

    ## finds post with specifc id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    ## grabs post
    post = post_query.first()

    ## if post doesn't exist return error
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was does not exist")

    ## update post_query with desired data
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user