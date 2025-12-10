from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services.skill_type_service import SkillTypeService
from ..schemas.skill_type import SkillTypeCreate, SkillTypeUpdate, SkillTypeResponse, SkillTypeRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=201)
def create_skill_type(payload: SkillTypeCreate, db: Session = Depends(get_db)):
    service = SkillTypeService(db)
    skill_type = service.create(payload)
    return {"success": True, "data": SkillTypeRead.from_orm(skill_type), "message": "Skill Type created successfully"}

@router.get("/", response_model=dict)
def list_skill_types(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    color: str | None = None,
    db: Session = Depends(get_db)
):
    service = SkillTypeService(db)
    result = service.list(page = page, limit = limit, search = search, is_active = is_active, color=color)
    result["items"] = [SkillTypeRead.from_orm(item) for item in result["items"]]
    return {'success': True, 'data': result}

@router.get("/{id}", response_model=dict)
def get_skill_type(id: int, db: Session = Depends(get_db)):
    service = SkillTypeService(db)
    skill_type = service.get(id)
    if not skill_type:
        raise HTTPException(status_code=404, detail="Skill Type not found")
    schema = SkillTypeRead.from_orm(skill_type)

    return {'success': True, 'data': schema}

@router.put("/{id}", response_model=dict)
def update_skill_type(id: int, payload: SkillTypeUpdate, db: Session = Depends(get_db)):
    service = SkillTypeService(db)
    record = service.update(id, payload)
    if not record:
        raise HTTPException(status_code=404, detail='Skill Type not found')

    schema = SkillTypeRead.from_orm(record)
    return {'success': True, 'data': schema, 'message': 'Skill Type updated successfully'}

@router.delete("/{id}",response_model=dict)
def delete_skill_type(id: int, db: Session = Depends(get_db)):
    service = SkillTypeService(db)
    return service.delete(id)
