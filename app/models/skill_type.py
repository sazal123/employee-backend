from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from ..db import Base
from datetime import datetime

class SkillType(Base):
    __tablename__ = "skill_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    color = Column(String(7), nullable=True)  # e.g., Hex color code
    sequence = Column(Integer, nullable=True)
    skills_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
