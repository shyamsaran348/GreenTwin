from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReminderBase(BaseModel):
    reminder_type: str
    next_due_date: datetime
    frequency: str

class ReminderCreate(ReminderBase):
    pass

class ReminderOut(ReminderBase):
    id: int
    plant_id: int
    is_completed: bool
    
    class Config:
        from_attributes = True
