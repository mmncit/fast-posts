from sqlalchemy import create_engine
import os

SQLALCHEMY_DATABASE_URL = os.environ['DB_URL']

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
