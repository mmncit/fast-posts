from sqlalchemy import String, func, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
from typing_extensions import Annotated
from typing import List

intpk = Annotated[int, mapped_column(primary_key=True)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()), ]


class Base(DeclarativeBase):
    pass


class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(300))
    content: Mapped[str] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(Boolean, server_default='FALSE')
    updated_at: Mapped[timestamp] = mapped_column(server_default=func.now(),
                                                  server_onupdate=func.now())
    created_at: Mapped[timestamp] = mapped_column(server_default=func.now())
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"))
    user: Mapped["User"] = relationship(back_populates="posts")


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[timestamp] = mapped_column(server_default=func.now())
    posts: Mapped[List["Posts"]] = relationship(back_populates="user",
                                                cascade="all, delete-orphan")
