from pydantic import BaseModel, Field


class TasksRead(BaseModel):
    id: int = Field(..., description='Индф пользователя')
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., )

    class Config:
        orm_mode = True


class TasksCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., )


class TasksUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., )
