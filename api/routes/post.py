from datetime import datetime
import random

from flask import Blueprint, request
from flask_pydantic import validate

from api.validation_schemas.post import PostCreateQueryParamsSchema, PostLikesQueryParamsSchema
from api.controllers.post_controller import PostController
from api.utils import authorize, make_response
from logger import log_func


post = Blueprint('post', __name__, template_folder='templates')


@post.route("/", methods=['POST'])
@log_func
@authorize(request)
@validate()
@make_response
def create(query: PostCreateQueryParamsSchema) -> None:
    content: str = query.content
    user_id: int = request.user_id
    post_data = {
        "user_id": user_id,
        "created_at": datetime.now(),
        "content": content,
    }
    PostController.validate_user_post_schema(post_data)
    PostController.create_new_user_post(post_data)


@post.route("/like", methods=['PUT'])
@log_func
@authorize(request)
@make_response
def like_post() -> None:
    user_id: int = request.user_id
    posts = PostController.get_posts()
    while True:
        n = random.randrange(0, len(posts))
        user_post = posts[n]
        post_data = {
            "user_id": user_id,
            "post_id": int(user_post.id),
            "created_at": datetime.now().date(),
        }
        PostController.validate_like_post_schema(post_data)
        is_liked: bool = PostController.check_if_post_already_liked_by_user(user_id, int(user_post.id))
        if not is_liked:
            PostController.like_post(post_data)
            break


@post.route("/dislike", methods=['PUT'])
@log_func
@authorize(request)
@make_response
def dislike_post() -> None:
    user_id: int = request.user_id
    posts = PostController.get_posts()
    while True:
        n = random.randrange(0, len(posts))
        user_post = posts[n]
        is_liked = PostController.check_if_post_already_liked_by_user(user_id, int(user_post.id))
        if is_liked:
            PostController.dislike_post(user_id, int(user_post.id))
            break


@post.route("/analytics", methods=['GET'])
@log_func
@validate()
@make_response
def get_analytics(query: PostLikesQueryParamsSchema) -> list:
    start_at: datetime = datetime.strptime(query.start_at, "%Y-%m-%d")
    end_at: datetime = datetime.strptime(query.end_at, "%Y-%m-%d")
    posts_likes = []
    raw_posts_likes = PostController.get_posts_likes(start_at, end_at)
    for raw_post in raw_posts_likes:
        posts_likes.append({
            "count": raw_post.count,
            "created_at": raw_post.created_at
        })
    return posts_likes
