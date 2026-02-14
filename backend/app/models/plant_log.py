from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class PlantLog(Base):
    __tablename__ = "plant_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    height = Column(Float) # in cm
    health_score = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    plant = relationship("app.models.plant.Plant", back_populates="logs")
