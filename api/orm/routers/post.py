from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from datetime import datetime, timezone

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), ):
    return db.query(models.Posts).all()


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_posts(post: schemas.PostBase,
                 db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
    # new_post = models.Posts(title=post.title,
    #                         content=post.content,
    #                         published=post.published)
    new_post = models.Posts(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    post_to_be_deleted = db.query(
        models.Posts).filter(models.Posts.id == id).first()
    print(post_to_be_deleted)
    if post_to_be_deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if current_user.id != post_to_be_deleted.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform requested action")

    db.delete(post_to_be_deleted)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,
                post: schemas.PostBase,
                db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    post_to_be_updated = db.query(
        models.Posts).filter(models.Posts.id == id).first()
    if post_to_be_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if current_user.id != post_to_be_updated.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform requested action")

    post_to_be_updated.content = post.content
    post_to_be_updated.title = post.title
    post_to_be_updated.published = post.published
    post_to_be_updated.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(post_to_be_updated)
    return post_to_be_updated