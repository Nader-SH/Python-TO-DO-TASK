from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.repositories.user_repository import login_user
from app.schemas.login import LoginUser, LoginUserRead
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user
from app.db.session import get_db
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/users", response_model=UserRead)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/login", response_model=LoginUserRead)
def api_login_user(user: LoginUser, response: Response, db: Session = Depends(get_db)):
    try:
        login_result = login_user(db, user)
        response.set_cookie(
            key="access_token",
            value=login_result["access_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return login_result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
