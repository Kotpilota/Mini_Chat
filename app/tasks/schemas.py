from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(...)
    description: str = Field(...)


class TaskUpdate(BaseModel):
    title: str = Field(...)
    description: str = Field(...)