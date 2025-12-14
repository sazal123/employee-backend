from pydantic import BaseModel
from datetime import datetime


class ResumeBase(BaseModel):
    title: str
    type: str


class ResumeCreate(ResumeBase):
    pass


class ResumeRead(ResumeBase):
    id: int
    employee_id: int
    file_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
