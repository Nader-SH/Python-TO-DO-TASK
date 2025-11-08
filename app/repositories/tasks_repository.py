from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.tasks import Tasks
from app.schemas.tasks import TaskCreate, TaskRead, TaskDeleteResponse, TaskUpdate, TaskUpdateResponse

def create_task(db: Session, task_in: TaskCreate, user_id: int):
    title = (task_in.title or "").strip()
    description = (task_in.description or "").strip()

    if not title or not description:
        raise ValueError("Title and description are required")

    existing_task = db.query(Tasks).filter(Tasks.title == title).first()
    if existing_task:
        raise ValueError("Title already exists")

    db_task = Tasks(
        title=title,
        description=description,
        completed=task_in.completed,
        user_id=user_id,
    )
    db.add(db_task)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Title already exists")
    db.refresh(db_task)
    return TaskRead(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
    )

def get_tasks(db: Session, user_id: int):
    return [
        TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
        for task in db.query(Tasks).filter(Tasks.user_id == user_id).all()
    ]

def delete_task(db: Session, task_id: int, user_id: int) -> TaskDeleteResponse:
    db_task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user_id).first()
    if not db_task:
        raise ValueError("Task not found")
    if db_task.completed:
        raise ValueError("You cannot delete a completed task")
    task_data = TaskRead(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
    )
    db.delete(db_task)
    db.commit()
    return TaskDeleteResponse(
        message=f"Task '{db_task.title}' deleted successfully",
        task=task_data,
    )

def update_task(db: Session, task_id: int, user_id: int, task_in: TaskUpdate) -> TaskUpdateResponse:
    db_task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user_id).first()
    if not db_task:
        raise ValueError("Task not found")
    if db_task.completed:
        raise ValueError("You cannot update a completed task")

    updated = False

    if task_in.title is not None:
        title = task_in.title.strip()
        if not title:
            raise ValueError("Title cannot be empty")
        existing = (
            db.query(Tasks)
            .filter(Tasks.title == title, Tasks.id != task_id)
            .first()
        )
        if existing:
            raise ValueError("Title already exists")
        db_task.title = title
        updated = True

    if task_in.description is not None:
        description = task_in.description.strip()
        if not description:
            raise ValueError("Description cannot be empty")
        db_task.description = description
        updated = True

    if task_in.completed is not None:
        db_task.completed = task_in.completed
        updated = True

    if not updated:
        raise ValueError("No fields provided to update")

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Title already exists")
    db.refresh(db_task)

    return TaskUpdateResponse(
        message=f"Task '{db_task.title}' updated successfully",
        task=TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
        ),
    )