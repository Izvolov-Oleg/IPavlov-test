from pydantic import BaseModel

class DataSchema(BaseModel):
    """Схема данных"""
    id: int
    value: str
    timestamp: int = None

    class Config:
        orm_mode = True
