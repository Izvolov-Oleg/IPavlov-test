from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from enum import Enum
from db import crud, schemas, models
from db.database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

# create table Data in DB
models.Base.metadata.create_all(bind=engine)


class FilterChoice(str, Enum):
    id = 'id'
    value = 'value'
    timestamp = 'timestamp'

# Our Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/data', response_model=List[schemas.DataSchema])
def get_data(
        id: int = Query(None, description="Filter for id"),
        value: str = Query(None, description="Filter for value"),
        timestamp: int = Query(None, description="Filter for timestamp"),
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db)
):
    data = crud.get_all_data(
        db=db,
        limit=limit,
        offset=offset,
        id=id,
        value=value,
        timestamp=timestamp)
    return data


@app.post('/data', response_model=schemas.DataSchema)
def post_data(data: schemas.DataSchema, db: Session = Depends(get_db)):
    return crud.create_data(db=db, data=data)


@app.put('/data')
def update_data(data: schemas.DataSchema, db: Session = Depends(get_db)):
    new_data = crud.check_update_data(db=db, data=data)
    if new_data is None:
        raise HTTPException(status_code=404,
                            detail="Data with this 'id' not found")
    return new_data
