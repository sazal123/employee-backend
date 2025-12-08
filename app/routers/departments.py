from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate
from ..services.department_service import DepartmentService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model=dict, status_code=201)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    service = DepartmentService(db)
    dept = service.create_department(payload)
    
    # Convert SQLAlchemy model to Pydantic schema
    dept_schema = DepartmentRead.from_orm(dept)

    return {'success': True, 'data': dept_schema, 'message': 'Department created successfully'}

@router.get('/', response_model=dict)
def list_departments(
    page: int = 1,
    limit: int = 10,
    search: str = None,
    is_active: bool = None,
    parent_department_id: int = None,
    db: Session = Depends(get_db)
):
    service = DepartmentService(db)
    result = service.list_departments(page=page, limit=limit, search=search,
                                      is_active=is_active, parent_department_id=parent_department_id)
    
    # Convert SQLAlchemy models to Pydantic
    result['items'] = [DepartmentRead.from_orm(dept) for dept in result['items']]
    
    return {'success': True, 'data': result}

@router.get('/{department_id}', response_model=dict)
def get_department(department_id: int, db: Session = Depends(get_db)):
    service = DepartmentService(db)
    dept = service.get_department(department_id)
    if not dept:
        raise HTTPException(status_code=404, detail='Department not found')

    dept_schema = DepartmentRead.from_orm(dept)
    return {'success': True, 'data': dept_schema}

@router.put("/{department_id}", response_model=dict)
def update_department(department_id: int, payload: DepartmentUpdate, db: Session = Depends(get_db)):
    service = DepartmentService(db)
    dept = service.update_department(department_id, payload)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    dept_schema = DepartmentRead.from_orm(dept)
    return {"success": True, "data": dept_schema, "message": "Department updated successfully"}

@router.delete("/{department_id}", response_model=dict)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    service = DepartmentService(db)
    dept = service.delete_department(department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    return {"success": True, "message": "Department deleted successfully"}

