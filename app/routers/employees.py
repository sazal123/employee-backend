from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import json

from ..db import SessionLocal
from ..services.employee_service import EmployeeService
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=201)
def create_employee(
    data: str = Form(...),
    profile_picture: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Parse JSON data from form
    payload = EmployeeCreate(**json.loads(data))
    service = EmployeeService(db)
    employee = service.create(payload, profile_picture)
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
def update_employee(
    id: int,
    data: str = Form(...),
    profile_picture: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Parse JSON data from form
    payload = EmployeeUpdate(**json.loads(data))
    service = EmployeeService(db)
    record = service.update(id, payload, profile_picture)
    if not record:
        raise HTTPException(status_code=404, detail='Employee not found')

    schema = EmployeeRead.from_orm(record)
    return {'success': True, 'data': schema, 'message': 'Employee updated successfully'}

@router.delete("/{id}", response_model=dict)
def delete_employee(id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.delete(id)
