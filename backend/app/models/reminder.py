from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    reminder_type = Column(String) # e.g., "water", "fertilizer"
    next_due_date = Column(DateTime)
    frequency = Column(String) # e.g., "daily", "weekly"
    is_completed = Column(Boolean, default=False)

    plant = relationship("app.models.plant.Plant", back_populates="reminders")
