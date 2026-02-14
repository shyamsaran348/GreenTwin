from pydantic import BaseModel
from datetime import datetime

class PlantStateBase(BaseModel):
    health_score: float
    growth_stage: str
    water_stress: float
    heat_stress: float
    disease_risk_index: float

class PlantStateOut(PlantStateBase):
    id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True
