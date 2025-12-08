# app/services/department_service.py
from sqlalchemy.orm import Session
from ..models.department import Department
from ..schemas.department import DepartmentUpdate, DepartmentRead

class DepartmentService:
    def __init__(self, db: Session):  # <-- ensure db is passed here
        self.db = db

    def create_department(self, payload):
        dept = Department(**payload.dict())
        self.db.add(dept)
        self.db.commit()
        self.db.refresh(dept)
        return dept

    def get_department(self, department_id: int):
        return self.db.query(Department).filter(Department.id == department_id).first()

    def list_departments(self, page=1, limit=10, search=None, is_active=None, parent_department_id=None):
        query = self.db.query(Department)

        if search:
            query = query.filter(Department.name.ilike(f"%{search}%"))
        if is_active is not None:
            query = query.filter(Department.is_active == is_active)
        if parent_department_id is not None:
            query = query.filter(Department.parent_department_id == parent_department_id)

        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }

    def update_department(self, department_id: int, payload: DepartmentUpdate):
        dept = self.db.query(Department).filter(Department.id == department_id).first()
        if not dept:
            return None

        for field, value in payload.dict(exclude_unset=True).items():
            setattr(dept, field, value)

        self.db.commit()
        self.db.refresh(dept)
        return dept

    def delete_department(self, department_id: int):
        dept = self.db.query(Department).filter(Department.id == department_id).first()
        if not dept:
            return None
        self.db.delete(dept)
        self.db.commit()
        return dept
