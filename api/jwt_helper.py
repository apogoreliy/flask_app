from datetime import datetime, timezone

import jwt

from config import config
from messages import messages
from logger import log_method


class JWTHelper:
    def __init__(self):
        jwt_info = {
            "SECRET": {
                "ACCESS_TOKEN": config["JWT_ACCESS_TOKEN"],
                "REFRESH_TOKEN": config["JWT_REFRESH_TOKEN"]
            },
            "LIFETIME": {
                "ACCESS_TOKEN": "7200",
                "REFRESH_TOKEN": "604800"
            },
            "ISSUER": "flask_app"
        }
        tokens = jwt_info["SECRET"]
        lifetimes = jwt_info["LIFETIME"]
        self._issuer: str = jwt_info["ISSUER"]
        self._access_token: str = tokens["ACCESS_TOKEN"]
        self._refresh_token: str = tokens["REFRESH_TOKEN"]
        self._access_token_secs_valid: int = int(lifetimes["ACCESS_TOKEN"])
        self._refresh_token_secs_valid: int = int(lifetimes["REFRESH_TOKEN"])

    @log_method
    def generate_auth_pair(self, user_id):
        timestamp_now = datetime.now(tz=timezone.utc).timestamp()
        payload = {
            "sub": user_id,
            "iss": self._issuer,
            "exp": int(timestamp_now + self._access_token_secs_valid)
        }
        access_token = jwt.encode(payload=payload, key=self._access_token, algorithm="HS256")

        payload["exp"] = timestamp_now + self._refresh_token_secs_valid
        refresh_token = jwt.encode(payload=payload, key=self._refresh_token, algorithm="HS256")

        result = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expiry": int(timestamp_now + self._access_token_secs_valid)
        }

        return result

    @log_method
    def _get_secret_by_token_type(self, token_type: str):
        token_types: dict = {
            "access_token": self._access_token,
            "refresh_token": self._refresh_token
        }

        secret = token_types.get(token_type)
        if not secret:
            raise Exception(messages["INVALID_TOKEN_TYPE"])

        return secret

    @log_method
    def get_decoded_claims_of_token(self, token, token_type: str = "access_token"):
        try:
            secret_key = self._get_secret_by_token_type(token_type)
            options = {
                "require": ["exp", "iss", "sub"]
            }

            claims = jwt.decode(
                jwt=token,
                key=secret_key,
                issuer=self._issuer,
                options=options,
                algorithms=["HS256"]
            )

            return claims
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            raise Exception(messages["TOKEN_EXPIRED"])

    @log_method
    def jwt_authorizer(self, authorization):
        token = authorization.split(" ")
        if len(token) != 2:
            raise Exception(messages["INVALID_TOKEN_FORMAT"])

        token = token[1]
        claims = self.get_decoded_claims_of_token(token)
        if not claims:
            raise Exception(messages["CLAIMS_NOT_FOUND"])

        user_id = int(claims["sub"])
        return user_id
