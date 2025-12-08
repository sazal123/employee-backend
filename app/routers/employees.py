from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas.employee import EmployeeCreate
from ..services.employee_service import EmployeeService
import shutil, os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', status_code=201, response_model=dict)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    emp = service.create_employee(payload)
    return {'success': True, 'data': emp, 'message': 'Employee created successfully'}

@router.get('/', response_model=dict)
def list_employees(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=200), search: str = None, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    result = service.list_employees(page=page, limit=limit, search=search)
    return {'success': True, 'data': result}

@router.get('/{employee_id}', response_model=dict)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    emp = service.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail='Employee not found')
    return {'success': True, 'data': emp}

@router.put('/{employee_id}/resume', response_model=dict)
def upload_resume(employee_id: int, file: UploadFile = File(...), description: str = Form(None), db: Session = Depends(get_db)):
    service = EmployeeService(db)
    emp = service.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail='Employee not found')
    uploads_dir = 'uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    filename = f'emp_{employee_id}_resume_{file.filename}'
    path = os.path.join(uploads_dir, filename)
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    service.attach_resume(emp, path)
    return {'success': True, 'data': {'employee_id': employee_id, 'resume_path': path, 'description': description}, 'message': 'Resume uploaded successfully'}
