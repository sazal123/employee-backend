from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..repositories.employee_repository import EmployeeRepository
from ..schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, db: Session):
        self.repo = EmployeeRepository(db)

    def create(self, data: EmployeeCreate):
        try:
            return self.repo.create(data)
        except IntegrityError as e:
            # check if the error is due to unique constraint on employee_code or email
            if "unique constraint" in str(e.orig).lower() or "duplicate" in str(e.orig).lower():
                if "employee_code" in str(e.orig).lower():
                    raise HTTPException(status_code=400, detail="Employee code already exists")
                elif "email" in str(e.orig).lower():
                    raise HTTPException(status_code=400, detail="Email already exists")
                raise HTTPException(status_code=400, detail="Employee already exists")
            raise HTTPException(status_code=500, detail="Internal server error")
    

    def list(self, page: int = 1, limit: int = 10, search: str = None, is_active = None, 
             department_id: int = None, employment_type: str = None):
        skip = (page - 1) * limit
        items, total = self.repo.get_all(
            skip=skip,
            limit=limit,
            search=search,
            is_active=is_active,
            department_id=department_id,
            employment_type=employment_type
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
            raise HTTPException(404, "Employee not found")
        return obj

    def update(self, id: int, data: EmployeeUpdate):
        obj = self.repo.update(id, data)
        if not obj:
            raise HTTPException(404, "Employee not found")
        return obj

    def delete(self, id: int):
        deleted = self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, "Employee not found")
        return {"message": "Deleted successfully"}
