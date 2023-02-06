from sqlalchemy import String, func, Text, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
from typing_extensions import Annotated

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
    updated_at: Mapped[timestamp] = mapped_column(server_onupdate=func.now())
    created_at: Mapped[timestamp] = mapped_column(server_default=func.now())

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, content={self.content!r}, published={self.published!r}, updated_at={self.updated_at!r}, created_at={self.created_at!r})"