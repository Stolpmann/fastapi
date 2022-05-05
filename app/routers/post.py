from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db


router = APIRouter(
    # hardcode http prefix to all post routers
    prefix = "/posts",

    # Group users together in /docs
    tags = ['Posts']
)


#HTTP GET REQUEST
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), search: Optional[str] = ""):
    ## Executes SQL query via cursor var
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).all()
    return posts

# HTTP POST REQUEST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# use path parameter ({id}) to get url of specific post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    ## returns
    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    ## finds post with specifc id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    ## grabs post
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "Not authroized to perform action")


    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

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

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "Not authroized to perform action")


    ## update post_query with desired data
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()