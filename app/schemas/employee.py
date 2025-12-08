from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import date, datetime

class Address(BaseModel):
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]

class EmergencyContact(BaseModel):
    name: Optional[str]
    relationship: Optional[str]
    phone: Optional[str]

class EmployeeCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    phone: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    nationality: Optional[str]
    national_id: Optional[str]
    department_id: Optional[int]
    job_position_id: Optional[int]
    job_title_id: Optional[int]
    work_location_id: Optional[int]
    manager_id: Optional[int]
    employment_type: Optional[str]
    date_of_joining: Optional[date]
    probation_end_date: Optional[date]
    salary: Optional[float]
    tag_ids: Optional[List[int]]
    is_active: Optional[bool] = True
    profile_picture: Optional[str]

class EmployeeRead(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: Optional[str]
    full_name: Optional[str]
    email: EmailStr
    phone: Optional[str]
    department: Optional[Any]
    job_position: Optional[Any]
    work_location: Optional[Any]
    is_active: bool
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
