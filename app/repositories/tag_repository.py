from sqlalchemy.orm import Session
from ..models.tag import Tag
from ..schemas.tag import TagCreate, TagUpdate

class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TagCreate):
        obj = Tag(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self, skip: int = 0, limit: int = 12, search: str = None, is_active: bool = None, code: str = None):
        query = self.db.query(Tag)

        if search:
            query = query.filter(Tag.name.ilike(f"%{search}%"))
        if is_active is not None:
            query = query.filter(Tag.is_active == is_active)
        if code is not None:
            query = query.filter(Tag.code.ilike(f"%{code}%"))

        q = query.order_by(Tag.id.asc())
        total = q.count()
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_by_id(self, id: int):
        return self.db.query(Tag).filter(Tag.id == id).first()

    def update(self, id: int, data: TagUpdate):
        obj = self.get_by_id(id)
        if not obj:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int):
        obj = self.get_by_id(id)
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return True
