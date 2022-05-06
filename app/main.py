from fastapi import FastAPI
from random import randrange
from . import models
from .database import engine, SessionLocal
from .routers import post, user, auth, vote


#Creates Tables in postgress
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# allows program to search post.py and user.py to check if any HTTP request match functions

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Path Operation
@app.get("/")
def root():
    return {"message": "Hello World"}

