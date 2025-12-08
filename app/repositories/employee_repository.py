from sqlalchemy.orm import Session
from ..models.employee import Employee

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, emp: Employee):
        self.db.add(emp)
        self.db.commit()
        self.db.refresh(emp)
        return emp

    def get(self, emp_id: int):
        return self.db.query(Employee).filter(Employee.id == emp_id).first()

    def list(self, skip: int = 0, limit: int = 10, search: str = None):
        q = self.db.query(Employee)
        if search:
            q = q.filter((Employee.first_name.ilike(f"%{search}%")) | (Employee.last_name.ilike(f"%{search}%")) | (Employee.employee_code.ilike(f"%{search}%")))
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total

    def update(self, emp: Employee):
        self.db.add(emp)
        self.db.commit()
        self.db.refresh(emp)
        return emp

    def delete(self, emp: Employee):
        self.db.delete(emp)
        self.db.commit()
