from sqlalchemy.orm import Session
from ..repositories.employee_repository import EmployeeRepository
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate
from datetime import date

class EmployeeService:
    def __init__(self, db: Session):
        self.repo = EmployeeRepository(db)

    def create_employee(self, payload: EmployeeCreate):
        emp = Employee(
            employee_code=payload.employee_code,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            phone=payload.phone,
            date_of_birth=payload.date_of_birth,
            gender=payload.gender,
            nationality=payload.nationality,
            national_id=payload.national_id,
            department_id=payload.department_id,
            job_position_id=payload.job_position_id,
            work_location_id=payload.work_location_id,
            manager_id=payload.manager_id,
            employment_type=payload.employment_type,
            date_of_joining=payload.date_of_joining,
            salary=payload.salary,
            tags=payload.tag_ids,
            is_active=payload.is_active,
            profile_picture=payload.profile_picture
        )
        return self.repo.create(emp)

    def get_employee(self, emp_id: int):
        return self.repo.get(emp_id)

    def list_employees(self, page: int = 1, limit: int = 10, search: str = None):
        skip = (page - 1) * limit
        items, total = self.repo.list(skip=skip, limit=limit, search=search)
        pages = (total + limit - 1) // limit if total else 0
        return {
            'items': items,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': pages
        }

    def attach_resume(self, emp, path: str):
        emp.resume_path = path
        return self.repo.update(emp)
