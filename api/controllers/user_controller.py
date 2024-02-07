from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update, Row

from api.validation_schemas.user import UserSignupSchema
from api.models import engine, User

from api.jwt_helper import JWTHelper

from messages import messages
from logger import log_func


class UserController:
    @staticmethod
    @log_func
    def validate_user_signup_schema(email: str, password_hash: str) -> dict:
        activity_at: datetime = datetime.now()
        user_data = {
            "email": email,
            "password_hash": password_hash,
            "created_at": activity_at,
            "logged_in_at": activity_at,
            "last_activity_at": activity_at,
        }
        UserSignupSchema(**user_data)
        return user_data

    @staticmethod
    @log_func
    def create_new_user(user_data: dict) -> int:
        with Session(engine) as session:
            new_user = User(**user_data)
            session.add(new_user)
            session.commit()
            user_id = int(new_user.id)
        return user_id

    @staticmethod
    @log_func
    def get_jwt_token(user_id) -> dict:
        token = JWTHelper().generate_auth_pair(user_id)
        return token

    @staticmethod
    @log_func
    def check_if_user_email_exists(email: str) -> bool:
        is_user_exist: bool = False
        with Session(engine) as session:
            user: Row = session.execute(select(User).where(User.email == email)).one_or_none()
            if user:
                is_user_exist = True
        return is_user_exist

    @staticmethod
    @log_func
    def get_user_id(email: str, password: str) -> int:
        user_id: int = 0
        with Session(engine) as session:
            user = session.scalars(
                select(User).where(User.email == email).where(User.password_hash == password)
            ).one_or_none()
            if user:
                user_id: int = user.id
        return user_id

    @staticmethod
    @log_func
    def update_login_at(user_id: int) -> None:
        with Session(engine) as session:
            session.execute(update(User).where(User.id == user_id).values(logged_in_at=datetime.now()))
            session.commit()

    @staticmethod
    @log_func
    def update_activity(user_id: int) -> None:
        with Session(engine) as session:
            session.execute(update(User).where(User.id == user_id).values(last_activity_at=datetime.now()))
            session.commit()

    @staticmethod
    @log_func
    def get_user_last_login_and_action(user_id: int) -> dict | Exception:
        with Session(engine) as session:
            users = session.scalars(select(User).where(User.id == user_id)).one_or_none()
            if not users:
                raise Exception(messages["USER_NOT_FOUND"])

            return {
                "last_activity_at": users.last_activity_at,
                "logged_in_at": users.logged_in_at
            }
