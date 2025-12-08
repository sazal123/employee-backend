from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    parent_department_id: Optional[int] = None
    manager_id: Optional[int] = None
    is_active: Optional[bool] = True

class DepartmentRead(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    parent_department_id: Optional[int] = None
    manager_id: Optional[int] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DepartmentUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str]
    parent_department_id: Optional[int]
    description: Optional[str]
    manager_id: Optional[int]
    is_active: Optional[bool]

    model_config = {
        "from_attributes": True
    }

class DepartmentDelete(BaseModel):
    id: int
