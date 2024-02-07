from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, delete, func

from api.validation_schemas.post import PostCreateSchema, PostLikeSchema
from api.models import engine, Post, PostLike

from logger import log_func


class PostController:
    @staticmethod
    @log_func
    def validate_user_post_schema(post_data: dict) -> None:
        PostCreateSchema(**post_data)

    @staticmethod
    @log_func
    def create_new_user_post(post_data: dict) -> None:
        with Session(engine) as session:
            new_user_post = Post(**post_data)
            session.add(new_user_post)
            session.commit()

    @staticmethod
    @log_func
    def get_posts():
        with Session(engine) as session:
            posts = session.scalars(select(Post)).all()
            return posts

    @staticmethod
    @log_func
    def validate_like_post_schema(post_data: dict) -> None:
        PostLikeSchema(**post_data)

    @staticmethod
    @log_func
    def like_post(post_data: dict) -> None:
        with Session(engine) as session:
            new_post_like = PostLike(**post_data)
            session.add(new_post_like)
            session.commit()

    @staticmethod
    @log_func
    def dislike_post(user_id: int, post_id: int) -> None:
        with Session(engine) as session:
            session.execute(delete(PostLike).where(PostLike.user_id == user_id).where(PostLike.post_id == post_id))
            session.commit()

    @staticmethod
    @log_func
    def check_if_post_already_liked_by_user(user_id: int, post_id: int):
        is_liked = False
        with Session(engine) as session:
            post_like = session.scalars(
                select(PostLike).where(PostLike.user_id == user_id).where(PostLike.post_id == post_id)
            ).one_or_none()

            if post_like:
                is_liked = True

        return is_liked

    @staticmethod
    @log_func
    def get_posts_likes(start_at: datetime, end_at: datetime):
        with Session(engine) as session:
            posts_likes = session.query(
                PostLike.created_at,
                func.count(PostLike.id).label('count')
            ).filter(
                PostLike.created_at.between(start_at, end_at)
            ).group_by(
                func.date(PostLike.created_at)
            ).all()
        return posts_likes
