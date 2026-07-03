from pydantic import BaseModel

from app.schemas.user import UserOut


class RegisterIn(BaseModel):
    username: str
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
