from pydantic import BaseModel
from datetime import datetime

class PlantLogBase(BaseModel):
    height: float
    health_score: float

class PlantLogCreate(BaseModel):
    height: float

class PlantLogOut(PlantLogBase):
    id: int
    recorded_at: datetime
    
    class Config:
        from_attributes = True
