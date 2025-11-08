from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.models.user import User
from app.schemas.login import LoginUser
from app.schemas.user import UserCreate

def _hash_password(raw_password: str) -> str:
    password_bytes = raw_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def create_user(db: Session, user_in: UserCreate):
    if not user_in.password:
        raise ValueError("Password is required")
    if not user_in.email:
        raise ValueError("Email is required")
    if not user_in.username:
        raise ValueError("Username is required")

    existing_by_email = db.query(User).filter(User.email == user_in.email).first()
    if existing_by_email:
        raise ValueError("Email already exists")

    existing_by_username = db.query(User).filter(User.username == user_in.username).first()
    if existing_by_username:
        raise ValueError("Username already exists")

    hashed_password = _hash_password(user_in.password)

    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def login_user(db: Session, user_in: LoginUser):
    if not user_in.email:
        raise ValueError("Email is required")
    if not user_in.password:
        raise ValueError("Password is required")
    existing_by_email = db.query(User).filter(User.email == user_in.email).first()
    if not existing_by_email:
        raise ValueError("Email Not Exists")

    if not bcrypt.checkpw(user_in.password.encode("utf-8"), existing_by_email.hashed_password.encode("utf-8")):
        raise ValueError("Password is incorrect Or Email")

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": existing_by_email.email,
        "user_id": existing_by_email.id,
        "exp": expire,
    }
    
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": existing_by_email,
    }

