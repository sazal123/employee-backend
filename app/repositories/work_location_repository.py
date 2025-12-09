from sqlalchemy.orm import Session
from ..models.work_location import WorkLocation
from ..schemas.work_location import WorkLocationCreate, WorkLocationUpdate

class WorkLocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: WorkLocationCreate):
        obj = WorkLocation(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self, page, limit, search, is_active, city, country):
        query = self.db.query(WorkLocation)
        if search:
            query = query.filter(WorkLocation.name.ilike(f"%{search}%"))
        if is_active is not None:
            query = query.filter(WorkLocation.is_active == is_active)
        if city:
            query = query.filter(WorkLocation.city == city)
        if country:
            query = query.filter(WorkLocation.country == country)
        return query.offset((page - 1) * limit).limit(limit).all()

    def get_by_id(self, id: int):
        return self.db.query(WorkLocation).filter(WorkLocation.id == id).first()

    def update(self, id: int, data: WorkLocationUpdate):
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
