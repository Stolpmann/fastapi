from fastapi import FastAPI
from fastapi.params import Body,Optional
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Path Operation
@app.get("/")
def root():
    return {"message": "Hello World"}

#HTTP GET REQUEST
@app.get("/posts")
def get_posts():
    return {"message": "Swag"}

# HTTP POST REQUEST
@app.post("/posts")
#Creates Function that takes pydantic model validates data and assigns it into a variable
def create_post(post: Post):
    print(post)
    #Converts Pydantic model into Dictionary
    print(post.dict())
    return {"data": post }

