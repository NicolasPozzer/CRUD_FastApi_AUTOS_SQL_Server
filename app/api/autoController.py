from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db import database
from app.model import autoModel
from app.schema import autoSch
from typing import List

autoModel.Base.metadata.create_all(bind=database.engine)


router = APIRouter()


# endpoints

@router.get("/autos", response_model=List[autoSch.Auto])
def read_autos(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    autos = db.query(autoModel.Auto).order_by(autoModel.Auto.id).offset(skip).limit(limit).all()
    return autos

@router.post("/autos/create", response_model=autoSch.Auto)
def create_auto(auto: autoSch.AutoCreate, db: Session = Depends(database.get_db)):
    db_auto = autoModel.Auto(**auto.dict())
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto

@router.get("/autos/find/{auto_id}", response_model=autoSch.Auto)
def read_auto(auto_id: int, db: Session = Depends(database.get_db)):
    db_auto = db.query(autoModel.Auto).filter(autoModel.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    return db_auto

@router.put("/autos/edit/{auto_id}", response_model=autoSch.Auto)
def update_auto(auto_id: int, auto: autoSch.AutoCreate, db: Session = Depends(database.get_db)):
    db_auto = db.query(autoModel.Auto).filter(autoModel.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    for key, value in auto.dict().items():
        setattr(db_auto, key, value)
    db.commit()
    db.refresh(db_auto)
    return db_auto

@router.delete("/autos/{auto_id}", response_model=autoSch.Auto)
def delete_auto(auto_id: int, db: Session = Depends(database.get_db)):
    db_auto = db.query(autoModel.Auto).filter(autoModel.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    db.delete(db_auto)
    db.commit()
    return db_auto
