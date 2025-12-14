import os
from sqlalchemy.orm import Session
from ..models.resume import Resume


class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, employee_id: int, title: str, resume_type: str, file_path: str):
        """Create a new resume record"""
        resume = Resume(
            employee_id=employee_id,
            title=title,
            type=resume_type,
            file_path=file_path
        )
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_by_id(self, id: int):
        """Get a resume by ID"""
        return self.db.query(Resume).filter(Resume.id == id).first()

    def get_by_employee(self, employee_id: int):
        """Get all resumes for an employee"""
        return self.db.query(Resume).filter(Resume.employee_id == employee_id).order_by(Resume.created_at.desc()).all()

    def delete(self, id: int):
        """Delete a resume"""
        resume = self.get_by_id(id)
        if not resume:
            return None
        
        # Delete the file
        if resume.file_path and os.path.exists(resume.file_path):
            try:
                os.remove(resume.file_path)
            except:
                pass
        
        self.db.delete(resume)
        self.db.commit()
        return True

    def upload_file(self, employee_id: int, employee_code: str, title: str, resume_type: str, resume_file):
        """Upload resume file and create database record"""
        import shutil
        
        # Save file
        uploads_dir = 'uploads/resumes'
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Get file extension
        file_extension = os.path.splitext(resume_file.filename)[1] or '.pdf'
        
        # Generate unique filename using timestamp
        import time
        timestamp = int(time.time() * 1000)
        filename = f"resume_{employee_code}_{timestamp}{file_extension}"
        file_path = os.path.join(uploads_dir, filename)
        
        # Save file
        try:
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(resume_file.file, buffer)
            
            # Create database record
            resume = self.create(employee_id, title, resume_type, file_path)
            return resume
        except Exception as e:
            print(f"Error saving resume: {e}")
            return None
