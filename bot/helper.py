import random

from bot.actions import Actions
from config import config
from logger import log_func, log_method


class Bot:
    @staticmethod
    @log_func
    def get_random_email(string_for_random_emails: str):
        email_length = 6
        email_provider = "@gmail"
        email_signs = []
        for i in range(email_length):
            n = random.randrange(0, len(string_for_random_emails))
            email_signs.append(string_for_random_emails[n])
        email = "".join([s for s in email_signs]) + email_provider
        return email

    @staticmethod
    @log_func
    def get_random_password(string_for_random_passwords: str):
        password_length = 10
        password_signs = []
        for i in range(password_length):
            n = random.randrange(0, len(string_for_random_passwords))
            password_signs.append(string_for_random_passwords[n])

        password = "".join([s for s in password_signs])
        return password

    @classmethod
    @log_method
    def create_users(cls) -> list[dict]:
        users = []
        for u in range(config["number_of_users"]):
            email = cls.get_random_email(config["string_for_random_emails"])
            password = cls.get_random_password(config["string_for_random_passwords"])
            token = Actions.signup_user(email, password)
            users.append({
                "email": email,
                "password": password,
                "token": token,
            })
        return users

    @staticmethod
    @log_func
    def get_random_post_content() -> str:
        content_length = 10
        words = config["strings_for_random_posts"]
        content_words = []
        for i in range(content_length):
            n = random.randrange(0, len(words))
            content_words.append(words[n])

        content = " ".join([c for c in content_words])
        return content

    @classmethod
    @log_method
    def create_user_posts(cls, token: str) -> None:
        for i in range(config["max_posts_per_user"]):
            content: str = cls.get_random_post_content()
            Actions.create_user_post(token, content)

    @classmethod
    @log_method
    def run_app_bot(cls):
        users = cls.create_users()
        for user in users:
            token: str = user["token"]
            cls.create_user_posts(token)

            for i in range(config["max_likes_per_user"]):
                Actions.like_posts(token)

            for i in range(config["max_dislikes_per_user"]):
                Actions.dislike_posts(token)

            Actions.login_user(user["email"], user["password"])
            Actions.get_user_activity(token)

        analytics = Actions.get_posts_analytics(config["start_at"], config["end_at"])
        print(analytics)

