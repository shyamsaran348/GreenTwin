from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import database
from app.models.user import User
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

@router.post("/location")
def update_location(
    loc_data: LocationUpdate, 
    db: Session = Depends(database.get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        current_user.latitude = loc_data.latitude
        current_user.longitude = loc_data.longitude
        db.commit()
        return {"message": "Location updated successfully"}
    except Exception as e:
        print(f"Error updating location: {e}")
        raise HTTPException(status_code=500, detail="Failed to update location")
