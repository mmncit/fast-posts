from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .database import engine
from .models import Base
from . import models, schemas

Base.metadata.create_all(engine)

app = FastAPI()


# Dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def test_connection(db: Session = Depends(get_db)):
    if db:
        return {"message": "success"}
    else:
        return {"message": "failed"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Posts).all()


@app.post("/posts",
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db)):
    # new_post = models.Posts(title=post.title,
    #                         content=post.content,
    #                         published=post.published)
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_to_be_deleted = db.query(
        models.Posts).filter(models.Posts.id == id).first()
    print(post_to_be_deleted)
    if post_to_be_deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    db.delete(post_to_be_deleted)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase,
                db: Session = Depends(get_db)):
    post_to_be_updated = db.query(
        models.Posts).filter(models.Posts.id == id).first()
    if post_to_be_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_to_be_updated.content = post.content
    post_to_be_updated.title = post.title
    post_to_be_updated.published = post.published
    post_to_be_updated.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(post_to_be_updated)
    return post_to_be_updated