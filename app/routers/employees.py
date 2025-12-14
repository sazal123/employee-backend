from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services.employee_service import EmployeeService
from ..services.resume_service import ResumeService
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeRead
from ..schemas.resume import ResumeRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=201)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    employee = service.create(payload)
    return {"success": True, "data": EmployeeRead.from_orm(employee), "message": "Employee created successfully"}

@router.get("/", response_model=dict)
def list_employees(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    department_id: int | None = None,
    employment_type: str | None = None,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    result = service.list(
        page=page, 
        limit=limit, 
        search=search, 
        is_active=is_active, 
        department_id=department_id,
        employment_type=employment_type
    )
    result["items"] = [EmployeeRead.from_orm(item) for item in result["items"]]
    return {'success': True, 'data': result}

@router.get("/{id}", response_model=dict)
def get_employee(id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    employee = service.get(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    schema = EmployeeRead.from_orm(employee)

    return {'success': True, 'data': schema}

@router.put("/{id}", response_model=dict)
def update_employee(id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    record = service.update(id, payload)
    if not record:
        raise HTTPException(status_code=404, detail='Employee not found')
    schema = EmployeeRead.from_orm(record)
    return {'success': True, 'data': schema, 'message': 'Employee updated successfully'}

@router.delete("/{id}", response_model=dict)
def delete_employee(id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.delete(id)

@router.post("/{employee_id}/upload-resume", response_model=dict)
async def upload_resume(
    employee_id: int,
    title: str = Form(...),
    type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    service = ResumeService(db)
    resume = service.upload_resume(employee_id, title, type, file)
    return {"success": True, "data": ResumeRead.from_orm(resume), "message": "Resume uploaded successfully"}

@router.get("/{employee_id}/resumes", response_model=dict)
def get_employee_resumes(employee_id: int, db: Session = Depends(get_db)):
    service = ResumeService(db)
    resumes = service.get_employee_resumes(employee_id)
    return {"success": True, "data": [ResumeRead.from_orm(resume) for resume in resumes]}

@router.delete("/{employee_id}/resumes/{resume_id}", response_model=dict)
def delete_resume(employee_id: int, resume_id: int, db: Session = Depends(get_db)):
    service = ResumeService(db)
    service.delete_resume(employee_id, resume_id)
    return {"success": True, "message": "Resume deleted successfully"}

@router.post("/{employee_id}/skills/{skill_id}", response_model=dict)
def attach_skill(employee_id: int, skill_id: int, db: Session = Depends(get_db)):
    """Attach a skill to an employee"""
    service = EmployeeService(db)
    employee = service.attach_skill(employee_id, skill_id)
    schema = EmployeeRead.from_orm(employee)
    return {'success': True, 'data': schema, 'message': 'Skill attached successfully'}

@router.delete("/{employee_id}/skills/{skill_id}", response_model=dict)
def remove_skill(employee_id: int, skill_id: int, db: Session = Depends(get_db)):
    """Remove a skill from an employee"""
    service = EmployeeService(db)
    employee = service.remove_skill(employee_id, skill_id)
    schema = EmployeeRead.from_orm(employee)
    return {'success': True, 'data': schema, 'message': 'Skill removed successfully'}
