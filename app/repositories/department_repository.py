from sqlalchemy.orm import Session
from ..models.department import Department

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, dept: Department):
        self.db.add(dept)
        self.db.commit()
        self.db.refresh(dept)
        return dept

    def get(self, dept_id: int):
        return self.db.query(Department).filter(Department.id == dept_id).first()

    def list(self, skip: int = 0, limit: int = 10, search: str = None, is_active: bool = None, parent_department_id: int = None):
        q = self.db.query(Department)
        if search:
            q = q.filter(Department.name.ilike(f"%{search}%"))
        if is_active is not None:
            q = q.filter(Department.is_active == is_active)
        if parent_department_id is not None:
            q = q.filter(Department.parent_department_id == parent_department_id)
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total

    def update(self, dept: Department):
        self.db.add(dept)
        self.db.commit()
        self.db.refresh(dept)
        return dept

    def delete(self, dept: Department):
        self.db.delete(dept)
        self.db.commit()
