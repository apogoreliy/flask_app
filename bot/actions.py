import requests

from api.utils import request_wrapper
from config import config

from logger import log_func


class Actions:
    @staticmethod
    @log_func
    @request_wrapper
    def signup_user(email: str, password: str):
        return requests.put(
            f"{config['host']}:{config['port']}/api/user/signup",
            params={"email": email, "password": password}
        )

    @staticmethod
    @log_func
    @request_wrapper
    def login_user(email: str, password: str):
        return requests.get(
            f"{config['host']}:{config['port']}/api/user/login",
            params={"email": email, "password": password}
        )

    @staticmethod
    @log_func
    @request_wrapper
    def get_user_activity(token: str):
        return requests.get(
            f"{config['host']}:{config['port']}/api/user/activity",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    @staticmethod
    @log_func
    @request_wrapper
    def create_user_post(token: str, content: str):
        return requests.post(
            f"{config['host']}:{config['port']}/api/post",
            headers={
                "Authorization": f"Bearer {token}"
            },
            params={
                "content": content
            }
        )

    @staticmethod
    @log_func
    @request_wrapper
    def like_posts(token: str):
        return requests.put(
            f"{config['host']}:{config['port']}/api/post/like",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

    @staticmethod
    @log_func
    @request_wrapper
    def dislike_posts(token: str):
        return requests.put(
            f"{config['host']}:{config['port']}/api/post/dislike",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

    @staticmethod
    @log_func
    @request_wrapper
    def get_posts_analytics(start_at: str, end_at: str):
        return requests.get(
            f"{config['host']}:{config['port']}/api/post/analytics",
            params={"start_at": start_at, "end_at": end_at}
        )
