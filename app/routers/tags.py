from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..services.tag_service import TagService
from ..schemas.tag import TagCreate, TagUpdate, TagRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=201)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)):
    service = TagService(db)
    tag = service.create(payload)
    return {"success": True, "data": TagRead.from_orm(tag), "message": "Tag created successfully"}

@router.get("/", response_model=dict)
def list_tags(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    is_active: bool | None = None,
    code: str | None = None,
    db: Session = Depends(get_db)
):
    service = TagService(db)
    result = service.list(page = page, limit = limit, search = search, is_active = is_active, code=code)
    result["items"] = [TagRead.from_orm(item) for item in result["items"]]
    return {'success': True, 'data': result}

@router.get("/{id}", response_model=dict)
def get_tag(id: int, db: Session = Depends(get_db)):
    service = TagService(db)
    tag = service.get(id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    schema = TagRead.from_orm(tag)

    return {'success': True, 'data': schema}

@router.put("/{id}", response_model=dict)
def update_tag(id: int, payload: TagUpdate, db: Session = Depends(get_db)):
    service = TagService(db)
    record = service.update(id, payload)
    if not record:
        raise HTTPException(status_code=404, detail='Tag not found')

    schema = TagRead.from_orm(record)
    return {'success': True, 'data': schema, 'message': 'Tag updated successfully'}

@router.delete("/{id}",response_model=dict)
def delete_tag(id: int, db: Session = Depends(get_db)):
    service = TagService(db)
    return service.delete(id)
