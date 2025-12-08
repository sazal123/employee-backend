from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------------------
# Job Position Create Schema
# ----------------------------
class JobPositionCreate(BaseModel):
    title: str
    code: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    level: Optional[str] = None
    is_active: Optional[bool] = True

# ----------------------------
# Job Position Read / Response Schema
# ----------------------------
class JobPositionRead(BaseModel):
    id: int
    title: str
    code: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    level: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ----------------------------
# Job Position Update Schema
# ----------------------------
class JobPositionUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[int] = None
    level: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

# ----------------------------
# Job Position Delete Schema
# ----------------------------
class JobPositionDelete(BaseModel):
    id: int
