from sqlalchemy.orm import Session
from app.repositories.user_repository import create_user as repo_create_user
from app.repositories.user_repository import login_user as repo_login_user
from app.schemas.login import LoginUser
from app.schemas.user import UserCreate

def create_user(db: Session, user_in: UserCreate):
    # validation here if needed for email fo something like that
    return repo_create_user(db, user_in)

def login_user(db: Session, user_in: LoginUser):
    return repo_login_user(db, user_in)