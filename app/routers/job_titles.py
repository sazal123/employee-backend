from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas.job_title import JobTitleCreate, JobTitleRead, JobTitleUpdate
from ..services.job_title_service import JobTitleService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=dict, status_code=201)
def create_job_title(payload: JobTitleCreate, db: Session = Depends(get_db)):
    service = JobTitleService(db)
    job_title = service.create_job_title(payload)
    return {"success": True, "data": JobTitleRead.from_orm(job_title), "message": "Job title created successfully"}


@router.get("/", response_model=dict)
def list_job_titles(
    page: int = 1,
    limit: int = 10,
    search: str = None,
    job_position_id: int = None,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    service = JobTitleService(db)
    result = service.list_job_titles(page, limit, search, job_position_id, is_active)
    result["items"] = [JobTitleRead.from_orm(item) for item in result["items"]]
    return {"success": True, "data": result}


@router.get("/{job_title_id}", response_model=dict)
def get_job_title(job_title_id: int, db: Session = Depends(get_db)):
    service = JobTitleService(db)
    job_title = service.get_job_title(job_title_id)
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    return {"success": True, "data": JobTitleRead.from_orm(job_title)}


@router.put("/{job_title_id}", response_model=dict)
def update_job_title(job_title_id: int, payload: JobTitleUpdate, db: Session = Depends(get_db)):
    service = JobTitleService(db)
    job_title = service.update_job_title(job_title_id, payload)
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    return {"success": True, "data": JobTitleRead.from_orm(job_title), "message": "Job title updated successfully"}


@router.delete("/{job_title_id}", response_model=dict)
def delete_job_title(job_title_id: int, db: Session = Depends(get_db)):
    service = JobTitleService(db)
    job_title = service.delete_job_title(job_title_id)
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    return {"success": True, "message": "Job title deleted successfully"}
