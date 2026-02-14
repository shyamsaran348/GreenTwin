from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import database
from app.models.reminder import Reminder
from app.models.plant import Plant
from app.models.user import User
from app.schemas.reminder_schema import ReminderCreate, ReminderOut
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"]
)

@router.post("/{plant_id}", response_model=ReminderOut)
def create_reminder(
    plant_id: int, 
    reminder: ReminderCreate, 
    db: Session = Depends(database.get_db), 
    current_user: User = Depends(get_current_user)
):
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
        
    new_reminder = Reminder(
        plant_id=plant_id,
        reminder_type=reminder.reminder_type,
        next_due_date=reminder.next_due_date,
        frequency=reminder.frequency
    )
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return new_reminder

@router.get("/", response_model=List[ReminderOut])
def get_reminders(db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return db.query(Reminder).join(Plant).filter(Plant.user_id == current_user.id).all()
