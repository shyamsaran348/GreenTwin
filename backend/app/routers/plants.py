from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app import database
from app.models.plant import Plant
from app.models.plant_state import PlantState
from app.models.user import User
from app.schemas.plant_schema import PlantCreate, PlantOut
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/plants",
    tags=["Plants"]
)

@router.get("/", response_model=List[PlantOut])
def get_plants(db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return db.query(Plant).filter(Plant.user_id == current_user.id).all()

@router.post("/", response_model=PlantOut)
def create_plant(plant: PlantCreate, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    new_plant = Plant(
        name=plant.name,
        species=plant.species,
        user_id=current_user.id
    )
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    
    # Initialize Plant State (Digital Twin)
    # Ideally this logic should be in a service, but for now simple init here
    new_state = PlantState(plant_id=new_plant.id)
    db.add(new_state)
    db.commit()
    
    return new_plant

@router.get("/{plant_id}", response_model=PlantOut)
def get_plant(plant_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    # Eager load plant_state to ensure it's available for the schema
    plant = db.query(Plant).options(joinedload(Plant.plant_state)).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@router.delete("/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    # Manual cascade delete for safety (or rely on DB cascade if configured)
    if plant.plant_state:
        db.delete(plant.plant_state)
        
    db.delete(plant)
    db.commit()
    return {"message": "Plant deleted successfully"}
