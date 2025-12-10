from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..repositories.skill_repository import SkillRepository
from ..schemas.skill import SkillCreate, SkillUpdate

class SkillService:
    def __init__(self, db: Session):
        self.repo = SkillRepository(db)

    def create(self, data: SkillCreate):
        try:
            return self.repo.create(data)
        except IntegrityError as e:
            # check if the error is due to unique constraint on name
            if "unique constraint" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise HTTPException(status_code=400, detail="Skill already exists")
            raise HTTPException(status_code=500, detail="Internal server error")
    

    def list(self, page: int = 1, limit: int = 10, search: str = None, is_active = None, skill_type_id: int = None):
        skip = (page - 1) * limit
        items, total = self.repo.get_all(
            skip=skip,
            limit=limit,
            search=search,
            skill_type_id=skill_type_id,
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
            raise HTTPException(404, "Skill not found")
        return obj

    def update(self, id: int, data: SkillUpdate):
        obj = self.repo.update(id, data)
        if not obj:
            raise HTTPException(404, "Skill not found")
        return obj

    def delete(self, id: int):
        deleted = self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, "Skill not found")
        return {"message": "Deleted successfully"}
