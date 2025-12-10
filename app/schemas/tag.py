from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TagBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TagRead(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TagList(BaseModel):
    items: list[TagRead]
    total: int
    page: int
    limit: int
    pages: int
