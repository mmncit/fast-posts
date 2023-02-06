import time
import os
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone

DATABASE = os.environ['DATABASE']
DB_USER = os.environ['DB_USER']
DB_HOST = os.environ['DB_HOST']
DB_PASSWORD = os.environ['DB_PASSWORD']


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()

# database connection
while True:

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor)  # to retrieve the column names
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "pass"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()  # push changes to db
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                   (str(id)))
    delete_post = cursor.fetchone()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s, updated_at = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, datetime.now(
            timezone.utc), str(id)))
    update_post = cursor.fetchone()
    conn.commit()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {"data": update_post}