from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    species = Column(String, index=True)
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("app.models.user.User", back_populates="plants")
    plant_state = relationship("app.models.plant_state.PlantState", uselist=False, back_populates="plant")
    disease_records = relationship("app.models.disease_record.DiseaseRecord", back_populates="plant")
    reminders = relationship("app.models.reminder.Reminder", back_populates="plant")
    logs = relationship("app.models.plant_log.PlantLog", back_populates="plant", cascade="all, delete-orphan")
