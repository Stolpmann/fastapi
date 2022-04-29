from pydantic import BaseModel, EmailStr
from datetime import datetime

#Creates Post Schema and defines data types
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

## Inherits Postbase class
class Post(PostBase):
    id: int
    created_at: datetime

    ## allows sql query to be converted to python dict
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
