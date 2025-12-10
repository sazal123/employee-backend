from pydantic import BaseModel
from typing import Optional

class SkillTypeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    color: Optional[str] = None  # e.g., Hex color code
    sequence: Optional[int] = None
    is_active: Optional[bool] = True

class SkillTypeCreate(SkillTypeBase):
    pass

class SkillTypeUpdate(SkillTypeBase):
    pass

class SkillTypeRead(SkillTypeBase):
    id: int

    class Config:
        from_attributes = True

class SkillTypeResponse(SkillTypeBase):
    id: int
    skills_count: int

    class Config:
        from_attributes = True
