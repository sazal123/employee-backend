from sqlalchemy.orm import Session, selectinload
from ..models.skill import Skill
from ..schemas.skill import SkillCreate, SkillUpdate

class SkillRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SkillCreate):
        obj = Skill(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self, skip: int = 0, limit: int = 12, search: str = None, is_active: bool = None, skill_type_id: int = None):
        query = self.db.query(Skill).options(selectinload(Skill.skill_type))

        if search:
            query = query.filter(Skill.name.ilike(f"%{search}%"))
        if is_active is not None:
            query = query.filter(Skill.is_active == is_active)
        if skill_type_id is not None:
            query = query.filter(Skill.skill_type_id == skill_type_id)

        q = query.order_by(Skill.id.asc())
        total = q.count()
        items = query.offset(skip).limit(limit).all()
        for item in items:
            item.skill_type_name = item.skill_type.name if item.skill_type else None

        return items, total

    def get_by_id(self, id: int):
        return self.db.query(Skill).filter(Skill.id == id).first()

    def update(self, id: int, data: SkillUpdate):
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
