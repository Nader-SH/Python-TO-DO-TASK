from typing import Optional
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        from_attributes = True


class TaskDeleteResponse(BaseModel):
    message: str
    task: TaskRead

class TaskUpdateResponse(BaseModel):
    message: str
    task: TaskRead