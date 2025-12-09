from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    parent_department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    manager_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    parent = relationship('Department', remote_side=[id])
    job_positions = relationship("JobPosition", back_populates="department")
