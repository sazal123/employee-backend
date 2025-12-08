from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repositories.job_position_repository import JobPositionRepository
from ..schemas.job_position import JobPositionCreate, JobPositionUpdate

class JobPositionService:

    def __init__(self, db: Session):
        self.repo = JobPositionRepository(db)

    def create(self, data: JobPositionCreate):
        return self.repo.create(data)

    def list(self, page, limit, search, department_id, level, is_active):
        return self.repo.get_all(page, limit, search, department_id, level, is_active)

    def get(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(404, "Job position not found")
        return obj

    def update(self, id: int, data: JobPositionUpdate):
        obj = self.repo.update(id, data)
        if not obj:
            raise HTTPException(404, "Job position not found")
        return obj

    def delete(self, id: int):
        deleted = self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, "Job position not found")
        return {"message": "Deleted successfully"}
