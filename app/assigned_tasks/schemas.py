from pydantic import BaseModel, Field
from datetime import datetime


class AssignedTasksCreate(BaseModel):
    task_title: str = Field(..., )
    status_id: int = Field(..., )


class AssignedTasksRead(BaseModel):
    id: int
    user_id: int
    task_id: int
    status_id: int
    deadline: datetime

    class Config:
        from_attributes = True


class AssignedTasksUpdate(BaseModel):
    status_id: int
