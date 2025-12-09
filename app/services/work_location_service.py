from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..repositories.work_location_repository import WorkLocationRepository
from ..schemas.work_location import WorkLocationCreate, WorkLocationUpdate

class WorkLocationService:
    def __init__(self, db: Session):
        self.repo = WorkLocationRepository(db)

    def create(self, data: WorkLocationCreate):
        try:
            return self.repo.create(data)
        except IntegrityError as e:
            # check if the error is due to unique constraint on code
            if "unique constraint" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise HTTPException(status_code=400, detail="Work Location already exists")
            raise HTTPException(status_code=500, detail="Internal server error")
    

    def list(self, page: int = 1, limit: int = 10, search: str = None, is_active = None, city = None, country = None):
        skip = (page - 1) * limit
        items, total = self.repo.get_all(
            skip=skip,
            limit=limit,
            search=search,
            city=city,
            country=country,
            is_active=is_active
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
            raise HTTPException(404, "Work location not found")
        return obj

    def update(self, id: int, data: WorkLocationUpdate):
        obj = self.repo.update(id, data)
        if not obj:
            raise HTTPException(404, "Work location not found")
        return obj

    def delete(self, id: int):
        deleted = self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, "Work location not found")
        return {"message": "Deleted successfully"}
