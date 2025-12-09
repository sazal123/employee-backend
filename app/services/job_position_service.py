from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repositories.job_position_repository import JobPositionRepository
from ..schemas.job_position import JobPositionCreate, JobPositionUpdate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class JobPositionService:

    def __init__(self, db: Session):
        self.repo = JobPositionRepository(db)

    def create(self, data: JobPositionCreate):
        try:
            return self.repo.create(data)
        except IntegrityError as e:
            # check if the error is due to unique constraint on code
            if "unique constraint" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise HTTPException(status_code=400, detail="Job Position already exists")
            raise HTTPException(status_code=500, detail="Internal server error")

    def list(self, page=1, limit=12, search = None, department_id = None, level = None, is_active = None ):

        skip = (page - 1) * limit

        items, total = self.repo.get_all(
            skip=skip,
            limit=limit,
            search=search,
            is_active=is_active,
            department_id=department_id,
            level=level,
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit,
        }

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
