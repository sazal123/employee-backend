from sqlalchemy.orm import Session
from ..models.job_title import JobTitle
from ..schemas.job_title import JobTitleCreate, JobTitleUpdate
from ..repositories.job_title_repository import JobTitleRepository
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class JobTitleService:
    def __init__(self, db: Session):
        self.repo = JobTitleRepository(db)

    def create_job_title(self, payload: JobTitleCreate):
        job_title = JobTitle(**payload.dict())
        try:
            return self.repo.create(job_title)
        except IntegrityError as e:
            # check if the error is due to unique constraint on code
            if "unique constraint" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise HTTPException(status_code=400, detail="Job Title already exists")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_job_title(self, id: int):
        return self.repo.get(id)

    def list_job_titles(self, page: int = 1, limit: int = 10, search: str = None, job_position_id: int = None, is_active: bool = None):
        skip = (page - 1) * limit
        return self.repo.list(skip=skip, limit=limit, search=search, job_position_id=job_position_id, is_active=is_active)

    def update_job_title(self, id: int, payload: JobTitleUpdate):
        obj = self.repo.get(id)
        if not obj:
            return None
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        return self.repo.update(obj)

    def delete_job_title(self, id: int):
        obj = self.repo.get(id)
        if not obj:
            return None
        return self.repo.delete(obj)
