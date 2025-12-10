from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate
import os
import shutil
from fastapi import UploadFile


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: EmployeeCreate, profile_picture_file: UploadFile = None):
        # Convert nested models to dict for JSON fields
        employee_data = data.dict()
        if employee_data.get('address'):
            employee_data['address'] = dict(employee_data['address'])
        if employee_data.get('emergency_contact'):
            employee_data['emergency_contact'] = dict(employee_data['emergency_contact'])
        
        # Handle profile picture upload
        if profile_picture_file:
            uploads_dir = 'uploads/profiles'
            os.makedirs(uploads_dir, exist_ok=True)
            # Generate unique filename using employee_code
            file_extension = os.path.splitext(profile_picture_file.filename)[1]
            filename = f"profile_{employee_data['employee_code']}{file_extension}"
            file_path = os.path.join(uploads_dir, filename)
            
            # Save the file
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(profile_picture_file.file, buffer)
            
            employee_data['profile_picture'] = file_path
        
        obj = Employee(**employee_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self, skip: int = 0, limit: int = 12, search: str = None, is_active: bool = None, 
                department_id: int = None, employment_type: str = None):
        query = self.db.query(Employee)

        if search:
            query = query.filter(
                (Employee.first_name.ilike(f"%{search}%")) | 
                (Employee.last_name.ilike(f"%{search}%")) | 
                (Employee.employee_code.ilike(f"%{search}%")) |
                (Employee.email.ilike(f"%{search}%"))
            )
        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)
        if department_id is not None:
            query = query.filter(Employee.department_id == department_id)
        if employment_type is not None:
            query = query.filter(Employee.employment_type.ilike(f"%{employment_type}%"))

        q = query.order_by(Employee.id.asc())
        total = q.count()
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_by_id(self, id: int):
        return self.db.query(Employee).filter(Employee.id == id).first()

    def update(self, id: int, data: EmployeeUpdate, profile_picture_file: UploadFile = None):
        obj = self.get_by_id(id)
        if not obj:
            return None
        
        update_data = data.dict(exclude_unset=True)
        # Convert nested models to dict for JSON fields
        if 'address' in update_data and update_data['address']:
            update_data['address'] = dict(update_data['address'])
        if 'emergency_contact' in update_data and update_data['emergency_contact']:
            update_data['emergency_contact'] = dict(update_data['emergency_contact'])
        
        # Handle profile picture upload
        if profile_picture_file:
            # Delete old profile picture if exists
            if obj.profile_picture and os.path.exists(obj.profile_picture):
                try:
                    os.remove(obj.profile_picture)
                except:
                    pass
            
            uploads_dir = 'uploads/profiles'
            os.makedirs(uploads_dir, exist_ok=True)
            # Generate unique filename using employee_code
            file_extension = os.path.splitext(profile_picture_file.filename)[1]
            filename = f"profile_{obj.employee_code}{file_extension}"
            file_path = os.path.join(uploads_dir, filename)
            
            # Save the file
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(profile_picture_file.file, buffer)
            
            update_data['profile_picture'] = file_path
        
        for key, value in update_data.items():
            setattr(obj, key, value)
        
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int):
        obj = self.get_by_id(id)
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return True
