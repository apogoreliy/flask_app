from typing import List
from sqlalchemy import ForeignKey, String, Integer, DATETIME, create_engine, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True,)
    email: Mapped[str] = mapped_column(String(128), unique=True,)
    password_hash: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[int] = mapped_column(DATETIME)
    logged_in_at: Mapped[int] = mapped_column(DATETIME)
    last_activity_at: Mapped[int] = mapped_column(DATETIME)
    post: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    created_at: Mapped[int] = mapped_column(DATETIME)
    content: Mapped[str] = mapped_column(String(500))
    user: Mapped["User"] = relationship(back_populates="post")


class PostLike(Base):
    __tablename__ = "post_like"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_account.id'), nullable=False)
    created_at: Mapped[int] = mapped_column(DATETIME)

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id'),
    )


engine = create_engine("sqlite:///app.db", echo=False, pool_size=5)
Base.metadata.create_all(engine)
