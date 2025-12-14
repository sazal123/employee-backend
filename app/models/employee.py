from sqlalchemy import Column, Integer, String, Boolean, Date, Float, JSON, ForeignKey, Text, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base


# Association table for employee-tag many-to-many relationship
employee_tags = Table(
    'employee_tags',
    Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    marital_status = Column(String(50), nullable=True)
    nationality = Column(String(100), nullable=True)
    national_id = Column(String(100), nullable=True)
    passport_number = Column(String(100), nullable=True)
    
    # Address stored as JSON
    address = Column(JSON, nullable=True)
    
    # Emergency contact stored as JSON
    emergency_contact = Column(JSON, nullable=True)
    
    # Foreign keys and relationships
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    job_position_id = Column(Integer, ForeignKey('job_positions.id'), nullable=True)
    job_title_id = Column(Integer, ForeignKey('job_titles.id'), nullable=True)
    work_location_id = Column(Integer, ForeignKey('work_locations.id'), nullable=True)
    manager_id = Column(Integer, nullable=True)  # Self-referential, nullable for now
    
    # Employment details
    employment_type = Column(String(50), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    probation_end_date = Column(Date, nullable=True)
    
    # Compensation and tags
    salary = Column(Float, nullable=True)
    work_shift_id = Column(Integer, nullable=True)
    
    # Status and media
    is_active = Column(Boolean, default=True)
    profile_picture = Column(String(500), nullable=True)
    resume_path = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    department = relationship('Department', backref='employees')
    job_position = relationship('JobPosition', backref='employees')
    job_title = relationship('JobTitle', backref='employees')
    work_location = relationship('WorkLocation', backref='employees')
    tags = relationship('Tag', secondary=employee_tags, backref='employees')
