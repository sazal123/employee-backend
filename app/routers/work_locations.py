from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services.work_location_service import WorkLocationService
from ..schemas.work_location import WorkLocationCreate, WorkLocationUpdate, WorkLocationResponse, WorrkLocationRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=201)
def create_work_location(payload: WorkLocationCreate, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    work_location = service.create(payload)
    return {"success": True, "data": WorrkLocationRead.from_orm(work_location), "message": "Worklocation created successfully"}

@router.get("/", response_model=dict)
def list_work_locations(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    city: str | None = None,
    country: str | None = None,
    db: Session = Depends(get_db)
):
    service = WorkLocationService(db)
    result = service.list(page = page, limit = limit, search = search, is_active = is_active, city = city, country = country)
    result["items"] = [WorrkLocationRead.from_orm(item) for item in result["items"]]
    return {'success': True, 'data': result}

@router.get("/{id}", response_model=dict)
def get_work_location(id: int, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    work_location = service.get(id)
    if not work_location:
        raise HTTPException(status_code=404, detail="Work location not found")
    schema = WorrkLocationRead.from_orm(work_location)

    return {'success': True, 'data': schema}

@router.put("/{id}", response_model=dict)
def update_work_location(id: int, payload: WorkLocationUpdate, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    record = service.update(id, payload)
    if not record:
        raise HTTPException(status_code=404, detail='Work Location not found')

    schema = WorrkLocationRead.from_orm(record)
    return {'success': True, 'data': schema, 'message': 'Work Location updated successfully'}

@router.delete("/{id}",response_model=dict)
def delete_work_location(id: int, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    return service.delete(id)
