from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DiseaseRecordBase(BaseModel):
    predicted_class: str
    confidence: float
    image_path: str

class DiseaseRecordOut(DiseaseRecordBase):
    id: int
    plant_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
