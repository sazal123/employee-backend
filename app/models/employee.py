from sqlalchemy import Column, Integer, String, Boolean, Date, Float, JSON, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    nationality = Column(String(100), nullable=True)
    national_id = Column(String(100), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    job_position_id = Column(Integer, nullable=True)
    work_location_id = Column(Integer, nullable=True)
    manager_id = Column(Integer, nullable=True)
    employment_type = Column(String(50), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    salary = Column(Float, nullable=True)
    tags = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    profile_picture = Column(String(500), nullable=True)
    resume_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    department = relationship('Department', backref='employees')
