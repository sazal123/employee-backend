from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db import Base
from datetime import datetime

class JobTitle(Base):
    __tablename__ = 'job_titles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    job_position_id = Column(Integer, ForeignKey('job_positions.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    job_position = relationship("JobPosition", back_populates="job_titles")
