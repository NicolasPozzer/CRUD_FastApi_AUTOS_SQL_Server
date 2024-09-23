from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.db import database
from app.model import autoModel
from app.schema import autoSch

autoModel.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

# get autos
@router.get("/autos", response_model=List[autoSch.Auto])
def read_autos(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    autos = db.query(autoModel.Auto).order_by(autoModel.Auto.id).offset(skip).limit(limit).all()
    return autos

# create auto (only admin)
@router.post("/autos/create", response_model=autoSch.Auto)
def create_auto(auto: autoSch.AutoCreate, db: Session = Depends(database.get_db), user_data: dict = Depends(get_current_user)):
    if "admin" not in user_data['roles']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_auto = autoModel.Auto(**auto.dict())
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto

# find auto for id
@router.get("/autos/find/{auto_id}", response_model=autoSch.Auto)
def read_auto(auto_id: int, db: Session = Depends(database.get_db)):
    db_auto = db.query(autoModel.Auto).filter(autoModel.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    return db_auto

# edit auto -> admin
@router.put("/autos/edit/{auto_id}", response_model=autoSch.Auto)
def update_auto(auto_id: int, auto: autoSch.AutoCreate, db: Session = Depends(database.get_db), user_data: dict = Depends(get_current_user)):
    if "admin" not in user_data['roles']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_auto = db.query(autoModel.Auto).filter(autoModel.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    for key, value in auto.dict().items():
        setattr(db_auto, key, value)
    db.commit()
    db.refresh(db_auto)
    return db_auto

# Delete auto - > admin
@router.delete("/autos/{auto_id}", response_model=autoSch.Auto)
def delete_auto(auto_id: int, db: Session = Depends(database.get_db), user_data: dict = Depends(get_current_user)):
    if "admin" not in user_data['roles']:  # verify if admin
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_auto = db.query(autoModel.Auto).filter(autoModel.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    db.delete(db_auto)
    db.commit()
    return db_auto
