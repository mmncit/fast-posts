from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models import Base
from .routers import post, user, auth

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def test_connection(db: Session = Depends(get_db)):
    if db:
        return {"message": "success"}
    else:
        return {"message": "failed"}
