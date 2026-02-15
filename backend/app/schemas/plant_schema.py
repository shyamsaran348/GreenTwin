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
from .disease_record_schema import DiseaseRecordOut

class PlantOut(PlantBase):
    id: int
    user_id: int
    created_at: datetime
    plant_state: Optional[PlantStateOut] = None
    logs: List[PlantLogOut] = []
    disease_records: List[DiseaseRecordOut] = []
    
    class Config:
        from_attributes = True
