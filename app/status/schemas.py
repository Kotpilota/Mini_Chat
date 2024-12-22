from pydantic import BaseModel, Field

class StatusCreate(BaseModel):
    title: str

class StatusUpdate(BaseModel):
    title: str
