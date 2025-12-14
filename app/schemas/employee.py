from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import date, datetime
from .tag import TagRead
from .skill import SkillRead


class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class EmergencyContact(BaseModel):
    name: Optional[str] = None
    relationship: Optional[str] = None
    phone: Optional[str] = None


class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    email: EmailStr
    phone: str
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    national_id: Optional[str] = None
    passport_number: Optional[str] = None
    address: Optional[Address] = None
    emergency_contact: Optional[EmergencyContact] = None
    department_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_title_id: Optional[int] = None
    work_location_id: Optional[int] = None
    manager_id: Optional[int] = None
    employment_type: Optional[str] = None
    date_of_joining: Optional[date] = None
    probation_end_date: Optional[date] = None
    salary: Optional[float] = None
    work_shift_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    is_active: Optional[bool] = True
    profile_picture: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    national_id: Optional[str] = None
    passport_number: Optional[str] = None
    address: Optional[Address] = None
    emergency_contact: Optional[EmergencyContact] = None
    department_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_title_id: Optional[int] = None
    work_location_id: Optional[int] = None
    manager_id: Optional[int] = None
    employment_type: Optional[str] = None
    date_of_joining: Optional[date] = None
    probation_end_date: Optional[date] = None
    salary: Optional[float] = None
    work_shift_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    is_active: Optional[bool] = True
    profile_picture: Optional[str] = None


class EmployeeRead(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    phone: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    marital_status: Optional[str]
    nationality: Optional[str]
    national_id: Optional[str]
    passport_number: Optional[str]
    address: Optional[dict]
    emergency_contact: Optional[dict]
    department_id: Optional[int]
    job_position_id: Optional[int]
    job_title_id: Optional[int]
    work_location_id: Optional[int]
    manager_id: Optional[int]
    employment_type: Optional[str]
    date_of_joining: Optional[date]
    probation_end_date: Optional[date]
    salary: Optional[float]
    work_shift_id: Optional[int]
    tags: Optional[List[TagRead]] = None
    skills: Optional[List[SkillRead]] = None
    is_active: bool
    profile_picture: Optional[str]
    resume_path: Optional[str]
    resume_title: Optional[str]
    resume_type: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmployeeList(BaseModel):
    items: list[EmployeeRead]
    total: int
    page: int
    limit: int
    pages: int
