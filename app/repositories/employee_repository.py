from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate
import os
import base64
import uuid


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def _save_profile_picture(self, employee_code: str, base64_image: str) -> str:
        """Save base64 encoded image to file system"""
        if not base64_image:
            return None
        
        try:
            # Check if it's a data URL (data:image/png;base64,...)
            if base64_image.startswith('data:image'):
                header, encoded = base64_image.split(',', 1)
                file_ext = header.split('/')[1].split(';')[0]
            else:
                encoded = base64_image
                file_ext = 'png'  # default
            
            # Decode base64
            image_data = base64.b64decode(encoded)
            
            # Create uploads directory
            uploads_dir = 'uploads/profiles'
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Generate filename
            filename = f"profile_{employee_code}.{file_ext}"
            file_path = os.path.join(uploads_dir, filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            return file_path
        except Exception as e:
            # If it's not base64 or fails, treat it as URL/path
            return base64_image

    def create(self, data: EmployeeCreate):
        # Convert nested models to dict for JSON fields
        employee_data = data.dict()
        if employee_data.get('address'):
            employee_data['address'] = dict(employee_data['address'])
        if employee_data.get('emergency_contact'):
            employee_data['emergency_contact'] = dict(employee_data['emergency_contact'])
        
        # Handle profile picture if it's base64
        if employee_data.get('profile_picture'):
            saved_path = self._save_profile_picture(
                employee_data['employee_code'], 
                employee_data['profile_picture']
            )
            employee_data['profile_picture'] = saved_path
        
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

    def update(self, id: int, data: EmployeeUpdate):
        obj = self.get_by_id(id)
        if not obj:
            return None
        
        update_data = data.dict(exclude_unset=True)
        # Convert nested models to dict for JSON fields
        if 'address' in update_data and update_data['address']:
            update_data['address'] = dict(update_data['address'])
        if 'emergency_contact' in update_data and update_data['emergency_contact']:
            update_data['emergency_contact'] = dict(update_data['emergency_contact'])
        
        # Handle profile picture if provided
        if 'profile_picture' in update_data and update_data['profile_picture']:
            # Delete old profile picture if exists
            if obj.profile_picture and os.path.exists(obj.profile_picture):
                try:
                    os.remove(obj.profile_picture)
                except:
                    pass
            
            saved_path = self._save_profile_picture(
                obj.employee_code, 
                update_data['profile_picture']
            )
            update_data['profile_picture'] = saved_path
        
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
