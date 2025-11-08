from sqlalchemy.orm import Session
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.repositories.tasks_repository import create_task as repo_create_task
from app.repositories.tasks_repository import get_tasks as repo_get_tasks
from app.repositories.tasks_repository import delete_task as repo_delete_task
from app.repositories.tasks_repository import update_task as repo_update_task
def create_task(db: Session, task_in: TaskCreate, user_id: int):
    return repo_create_task(db, task_in, user_id)

def get_tasks(db: Session, user_id: int):
    return repo_get_tasks(db, user_id)

def delete_task(db: Session, task_id: int, user_id: int):
    return repo_delete_task(db, task_id, user_id)

def update_task(db: Session, task_id: int, user_id: int, task_in: TaskUpdate):
    return repo_update_task(db, task_id, user_id, task_in)