from sqlalchemy import create_engine
import os
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = os.environ['DB_URL']

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


# Dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()