from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..repositories.resume_repository import ResumeRepository
from ..repositories.employee_repository import EmployeeRepository


class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ResumeRepository(db)
        self.employee_repo = EmployeeRepository(db)

    def upload_resume(self, employee_id: int, title: str, resume_type: str, resume_file):
        """Upload a resume for an employee"""
        # Check if employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(404, "Employee not found")
        
        # Upload file and create record
        resume = self.repo.upload_file(employee_id, employee.employee_code, title, resume_type, resume_file)
        if not resume:
            raise HTTPException(500, "Failed to upload resume")
        
        return resume

    def get_employee_resumes(self, employee_id: int):
        """Get all resumes for an employee"""
        # Check if employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(404, "Employee not found")
        
        return self.repo.get_by_employee(employee_id)

    def delete_resume(self, employee_id: int, resume_id: int):
        """Delete a resume"""
        # Check if employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(404, "Employee not found")
        
        # Get resume and verify it belongs to the employee
        resume = self.repo.get_by_id(resume_id)
        if not resume:
            raise HTTPException(404, "Resume not found")
        
        if resume.employee_id != employee_id:
            raise HTTPException(403, "Resume does not belong to this employee")
        
        deleted = self.repo.delete(resume_id)
        if not deleted:
            raise HTTPException(404, "Resume not found")
        
        return True
