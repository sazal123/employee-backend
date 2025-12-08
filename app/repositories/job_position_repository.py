from sqlalchemy.orm import Session
from ..models.job_position import JobPosition
from ..schemas.job_position import JobPositionCreate, JobPositionUpdate

class JobPositionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: JobPositionCreate):
        obj = JobPosition(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self, page, limit, search, department_id, level, is_active):
        query = self.db.query(JobPosition)

        if search:
            query = query.filter(JobPosition.title.ilike(f"%{search}%"))

        if department_id:
            query = query.filter(JobPosition.department_id == department_id)

        if level:
            query = query.filter(JobPosition.level == level)

        if is_active is not None:
            query = query.filter(JobPosition.is_active == is_active)

        return query.offset((page - 1) * limit).limit(limit).all()

    def get_by_id(self, id: int):
        return self.db.query(JobPosition).filter(JobPosition.id == id).first()

    def update(self, id: int, data: JobPositionUpdate):
        obj = self.get_by_id(id)
        if not obj:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int):
        obj = self.get_by_id(id)
        if not obj:
            return None

        self.db.delete(obj)
        self.db.commit()
        return True
