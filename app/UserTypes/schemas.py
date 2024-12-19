from pydantic import BaseModel, Field


class UserTypeRead(BaseModel):
    id: int = Field(..., description='Индф пользователя')
    usertype: str = Field(..., min_length=3, max_length=50)


class UserTypeCreate(BaseModel):
    usertype: str = Field(..., min_length=3, max_length=50)


class UserTypeUpdate(BaseModel):
    usertype: str = Field(...,  min_length=3, max_length=50)
