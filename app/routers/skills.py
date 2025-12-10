from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services.skill_service import SkillService
from ..schemas.skill import SkillCreate, SkillUpdate, SkillRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=201)
def create_skill(payload: SkillCreate, db: Session = Depends(get_db)):
    service = SkillService(db)
    skill = service.create(payload)
    return {"success": True, "data": SkillRead.from_orm(skill), "message": "Skill created successfully"}

@router.get("/", response_model=dict)
def list_skills(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    skill_type_id: int | None = None,
    db: Session = Depends(get_db)
):
    service = SkillService(db)
    result = service.list(page = page, limit = limit, search = search, is_active = is_active, skill_type_id=skill_type_id)
    result["items"] = [SkillRead.from_orm(item) for item in result["items"]]
    return {'success': True, 'data': result}

@router.get("/{id}", response_model=dict)
def get_skill(id: int, db: Session = Depends(get_db)):
    service = SkillService(db)
    skill = service.get(id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    schema = SkillRead.from_orm(skill)

    return {'success': True, 'data': schema}

@router.put("/{id}", response_model=dict)
def update_skill(id: int, payload: SkillUpdate, db: Session = Depends(get_db)):
    service = SkillService(db)
    record = service.update(id, payload)
    if not record:
        raise HTTPException(status_code=404, detail='Skill not found')

    schema = SkillRead.from_orm(record)
    return {'success': True, 'data': schema, 'message': 'Skill updated successfully'}

@router.delete("/{id}",response_model=dict)
def delete_skill(id: int, db: Session = Depends(get_db)):
    service = SkillService(db)
    return service.delete(id)
