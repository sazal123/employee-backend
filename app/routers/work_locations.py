from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services.work_location_service import WorkLocationService
from ..schemas.work_location import WorkLocationCreate, WorkLocationUpdate, WorkLocationResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=WorkLocationResponse)
def create_work_location(payload: WorkLocationCreate, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    return service.create(payload)

@router.get("/", response_model=list[WorkLocationResponse])
def list_work_locations(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str | None = None,
    is_active: bool | None = None,
    city: str | None = None,
    country: str | None = None,
    db: Session = Depends(get_db)
):
    service = WorkLocationService(db)
    return service.list(page, limit, search, is_active, city, country)

@router.get("/{id}", response_model=WorkLocationResponse)
def get_work_location(id: int, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    return service.get(id)

@router.put("/{id}", response_model=WorkLocationResponse)
def update_work_location(id: int, payload: WorkLocationUpdate, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    return service.update(id, payload)

@router.delete("/{id}")
def delete_work_location(id: int, db: Session = Depends(get_db)):
    service = WorkLocationService(db)
    return service.delete(id)
