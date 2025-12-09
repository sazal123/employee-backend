from sqlalchemy.orm import Session
from ..models.job_title import JobTitle

class JobTitleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj: JobTitle):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, id: int):
        return self.db.query(JobTitle).filter(JobTitle.id == id).first()

    def list(self, skip: int = 0, limit: int = 12, search: str = None, job_position_id: int = None, is_active: bool = None):
        query = self.db.query(JobTitle)
        if search:
            query = query.filter(JobTitle.name.ilike(f"%{search}%"))
        if job_position_id:
            query = query.filter(JobTitle.job_position_id == job_position_id)
        if is_active is not None:
            query = query.filter(JobTitle.is_active == is_active)

        q = q.order_by(JobTitle.id.asc())
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return {"total": total, "items": items}

    def update(self, obj: JobTitle):
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: JobTitle):
        self.db.delete(obj)
        self.db.commit()
        return obj
