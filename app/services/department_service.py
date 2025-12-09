from sqlalchemy.orm import Session
from ..models.department import Department
from ..schemas.department import DepartmentUpdate, DepartmentRead
from ..repositories.department_repository import DepartmentRepository
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class DepartmentService:
    def __init__(self, db: Session):
        self.repo = DepartmentRepository(db)

    def create_department(self, payload):
        dept = Department(**payload.dict())
        try:
            return self.repo.create(dept)
        except IntegrityError as e:
            # check if the error is due to unique constraint on code
            if "unique constraint" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                raise HTTPException(status_code=400, detail="Department code already exists")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_department(self, department_id: int):
        return self.repo.get(department_id)

    def list_departments(self, page=1, limit=12, search=None, is_active=None, parent_department_id=None):
        skip = (page - 1) * limit

        items, total = self.repo.list(
            skip=skip,
            limit=limit,
            search=search,
            is_active=is_active,
            parent_department_id=parent_department_id,
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit,
        }

    def update_department(self, department_id: int, payload: DepartmentUpdate):
        dept = self.repo.get(department_id)
        if not dept:
            return None

        for field, value in payload.dict(exclude_unset=True).items():
            setattr(dept, field, value)

        return self.repo.update(dept)

    def delete_department(self, department_id: int):
        dept = self.repo.get(department_id)
        if not dept:
            return None

        return self.repo.delete(dept)
