from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SkillBase(BaseModel):
    name: str
    skill_type_id: int
    description: Optional[str] = None
    is_active: Optional[bool] = True


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    skill_type_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SkillRead(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime
    skill_type_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class SkillList(BaseModel):
    items: list[SkillRead]
    total: int
    skip: int
    limit: int
