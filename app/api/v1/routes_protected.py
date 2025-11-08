from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_active_user
from app.db.session import get_db
from app.schemas.tasks import TaskCreate, TaskRead, TaskDeleteResponse, TaskUpdateResponse, TaskUpdate
from app.schemas.user import UserRead
from app.services.tasks_service import (
    create_task,
    delete_task,
    get_tasks,
    update_task as service_update_task,
)
router = APIRouter()

@router.get("/auth/me", response_model=UserRead)
def api_get_current_user(current_user: UserRead = Depends(get_current_active_user)):
    return current_user

@router.post("/auth/tasks", response_model=TaskCreate)
def api_create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_active_user)):
    try:
        return create_task(db, task, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.get("/auth/tasks", response_model=List[TaskRead])
def api_get_tasks(db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_active_user)):
    try:
        return get_tasks(db, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.delete("/auth/tasks/{task_id}", response_model=TaskDeleteResponse)
def api_delete_task(task_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_active_user)):
    try:
        return delete_task(db, task_id, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.put("/auth/tasks/{task_id}", response_model=TaskUpdateResponse)
def api_update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_active_user)):
    try:
        return service_update_task(db, task_id, current_user.id, task)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))