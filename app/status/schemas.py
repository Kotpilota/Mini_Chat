from pydantic import BaseModel, Field

class StatusCreate(BaseModel):
    title: str = Field(...)


class StatusUpdate(BaseModel):
    title: str = Field(...)