from datetime import datetime

from pydantic import BaseModel


class UserSignupSchema(BaseModel):
    email: str
    password_hash: str
    created_at: datetime | None
    logged_in_at: datetime | None
    last_activity_at: datetime | None


class UserSignupQueryParamsSchema(BaseModel):
    email: str
    password: str
