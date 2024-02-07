from flask import Blueprint, request
from flask_pydantic import validate


from api.validation_schemas.user import UserSignupQueryParamsSchema
from api.controllers.user_controller import UserController
from api.utils import authorize, make_response, hash_password

from messages import messages
from logger import log_func

user = Blueprint('user', __name__, template_folder='templates')


@user.route("/signup", methods=['PUT'])
@log_func
@validate()
@make_response
def signup(query: UserSignupQueryParamsSchema):
    password_hash = hash_password(query.password)
    user_data = UserController.validate_user_signup_schema(query.email, password_hash)
    is_user_exist = UserController.check_if_user_email_exists(query.email)
    if is_user_exist:
        raise Exception(messages["USER_ALREADY_EXISTS"])

    user_id = UserController.create_new_user(user_data)
    token = UserController.get_jwt_token(user_id)
    return token["access_token"]


@user.route("/login", methods=['GET'])
@log_func
@validate()
@make_response
def login(query: UserSignupQueryParamsSchema):
    password_hash = hash_password(query.password)
    user_id = UserController.get_user_id(query.email, password_hash)
    if not user_id:
        raise Exception(messages["USER_NOT_FOUND"])

    UserController.update_login_at(user_id)
    token = UserController.get_jwt_token(user_id)
    return token["access_token"]


@user.route("/activity", methods=['GET'])
@log_func
@authorize(request)
@make_response
def get_user_activities():
    activities: dict = UserController.get_user_last_login_and_action(request.user_id)
    return activities
