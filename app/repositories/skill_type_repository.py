from sqlalchemy.orm import Session
from ..models.skill_type import SkillType
from ..schemas.skill_type import SkillTypeCreate, SkillTypeUpdate

class SkillTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SkillTypeCreate):
        obj = SkillType(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self, skip: int = 0, limit: int = 12, search: str = None, is_active: bool = None, color: str = None):
        query = self.db.query(SkillType)

        if search:
            query = query.filter(SkillType.name.ilike(f"%{search}%"))
        if is_active is not None:
            query = query.filter(SkillType.is_active == is_active)
        if color is not None:
            query = query.filter(SkillType.color.ilike(f"%{color}%"))

        q = query.order_by(SkillType.id.asc())
        total = q.count()
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_by_id(self, id: int):
        return self.db.query(SkillType).filter(SkillType.id == id).first()

    def update(self, id: int, data: SkillTypeUpdate):
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
