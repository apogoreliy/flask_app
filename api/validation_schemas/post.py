from datetime import datetime

from pydantic import BaseModel


class PostCreateSchema(BaseModel):
    user_id: int
    created_at: datetime
    content: str


class PostCreateQueryParamsSchema(BaseModel):
    content: str


class PostLikesQueryParamsSchema(BaseModel):
    start_at: str
    end_at: str


class PostLikeSchema(BaseModel):
    user_id: int
    post_id: int
    created_at: datetime
