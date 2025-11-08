from pydantic import BaseModel, EmailStr

from app.schemas.user import UserRead


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class LoginUserRead(BaseModel):
    access_token: str
    token_type: str
    user: UserRead

    class Config:
        from_attributes = True
