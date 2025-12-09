from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobTitleCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    job_position_id: int
    is_active: Optional[bool] = True

class JobTitleRead(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    job_position_id: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobTitleUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    job_position_id: Optional[int]
    is_active: Optional[bool]
    class Config:
        from_attributes = True

class JobTitleDelete(BaseModel):
    id: int
