from pydantic import BaseModel

class AutoBase(BaseModel):
    marca: str

class AutoCreate(AutoBase):
    pass

class Auto(AutoBase):
    id: int

    class Config:
        from_attributes = True
