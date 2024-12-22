from datetime import datetime

from pydantic import BaseModel


class AssignedTaskCreate(BaseModel):
    user_id: int
    task_id: int
    status_id: int
    deadline: datetime


class AssignedTaskUpdate(BaseModel):
    user_id: int
    task_id: int
    status_id: int
    deadline: datetime
