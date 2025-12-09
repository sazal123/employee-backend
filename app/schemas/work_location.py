from pydantic import BaseModel
from typing import Optional

class WorkLocationBase(BaseModel):
    name: str
    code: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_active: Optional[bool] = True

class WorkLocationCreate(WorkLocationBase):
    pass

class WorkLocationUpdate(WorkLocationBase):
    pass

class WorrkLocationRead(WorkLocationBase):
    id: int
    name: str
    code: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    phone: str
    email: str
    latitude: float
    longitude: float
    is_active: bool = True
    class Config:
        from_attributes = True

class WorkLocationResponse(WorkLocationBase):
    id: int

    class Config:
        from_attributes = True
