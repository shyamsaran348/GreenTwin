from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .plant_state_schema import PlantStateOut

class PlantBase(BaseModel):
    name: str
    species: str

class PlantCreate(PlantBase):
    pass

from .plant_log_schema import PlantLogOut

class PlantOut(PlantBase):
    id: int
    user_id: int
    created_at: datetime
    plant_state: Optional[PlantStateOut] = None
    logs: List[PlantLogOut] = []
    
    class Config:
        from_attributes = True
