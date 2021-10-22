from sqlalchemy import or_
from sqlalchemy.orm import Session
from . import models, schemas


def check_update_data(db: Session, data: schemas.DataSchema):
    our_data = db.query(models.Data).filter(models.Data.id == data.id).first()
    if our_data:
        our_data.value = data.value
        db.commit()
        db.refresh(our_data)
        return our_data
    return None


def get_all_data(
        db: Session,
        offset: int,
        limit: int,
        id: int,
        value: str,
        timestamp: int):
    if value or id or timestamp:
        return db.query(models.Data). filter(or_(models.Data.id == id,
                                                 models.Data.value == value,
                                                 models.Data.timestamp == timestamp)).offset(offset).limit(limit).all()
    return db.query(models.Data).offset(offset).limit(limit).all()

def create_data(db: Session, data: schemas.DataSchema):
    db_data = models.Data(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
