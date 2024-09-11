from sqlalchemy import Column, Integer, String
from ..db.database import Base

class Auto(Base):
    __tablename__ = "autos"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(255), index=True)