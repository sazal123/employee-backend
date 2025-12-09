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

class WorkLocationResponse(WorkLocationBase):
    id: int

    class Config:
        from_attributes = True
