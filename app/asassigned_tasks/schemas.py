from datetime import datetime

from pydantic import BaseModel, Field


class AssignedTaskCreate(BaseModel):
    user_id: int = Field(...)
    task_id: int = Field(...)
    status_id: int = Field(...)
    deadline: datetime = Field(...)


class AssignedTaskUpdate(BaseModel):
    user_id: int = Field(...)
    task_id: int = Field(...)
    status_id: int = Field(...)
    deadline: datetime = Field(...)