from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..schemas.job_position import JobPositionCreate, JobPositionUpdate, JobPositionRead
from ..services.job_position_service import JobPositionService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 2.1 Create Job Position
@router.post('/', response_model=dict, status_code=201)
def create_job_position(payload: JobPositionCreate, db: Session = Depends(get_db)):
    service = JobPositionService(db)
    record = service.create(payload)

    schema = JobPositionRead.from_orm(record)

    return {'success': True, 'data': schema, 'message': 'Job Position created successfully'}


# 2.2 List Job Positions
@router.get("/", response_model=dict)
def list_job_positions(
    page: int = 1, limit: int = 10,
    search: str = None,
    department_id: int = None,
    level: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    service = JobPositionService(db)
    items = service.list(page, limit, search, department_id, level, is_active)
    
    # Convert to Pydantic schemas
    job_positions = [JobPositionRead.from_orm(item) for item in items]
    return {"success": True, "data": job_positions}



# 2.3 Get Job Position by ID
@router.get('/{position_id}', response_model=dict)
def get_job_position(position_id: int, db: Session = Depends(get_db)):
    service = JobPositionService(db)
    record = service.get(position_id)

    if not record:
        raise HTTPException(status_code=404, detail='Job Position not found')

    schema = JobPositionRead.from_orm(record)
    return {'success': True, 'data': schema}


# 2.4 Update Job Position
@router.put('/{position_id}', response_model=dict)
def update_job_position(position_id: int, payload: JobPositionUpdate, db: Session = Depends(get_db)):
    service = JobPositionService(db)
    record = service.update(position_id, payload)

    if not record:
        raise HTTPException(status_code=404, detail='Job Position not found')

    schema = JobPositionRead.from_orm(record)
    return {'success': True, 'data': schema, 'message': 'Job Position updated successfully'}


# 2.5 Delete Job Position
@router.delete('/{position_id}', response_model=dict)
def delete_job_position(position_id: int, db: Session = Depends(get_db)):
    service = JobPositionService(db)
    deleted = service.delete(position_id)

    if not deleted:
        raise HTTPException(status_code=404, detail='Job Position not found')

    return {'success': True, 'message': 'Job Position deleted successfully'}
