from sqlalchemy import Column, String, Integer
from .database import Base


class Data(Base):
    """Таблица наших данных"""
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, unique=True)
    value = Column(String)
    timestamp = Column(Integer, default=None)
