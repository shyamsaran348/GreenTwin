from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class PlantState(Base):
    __tablename__ = "plant_states"
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), unique=True)
    health_score = Column(Float, default=100.0)
    growth_stage = Column(String, default="seedling")
    water_stress = Column(Float, default=0.0) # 0 to 1
    heat_stress = Column(Float, default=0.0)  # 0 to 1
    disease_risk_index = Column(Float, default=0.0) # 0 to 1
    last_updated = Column(DateTime, default=datetime.utcnow)

    plant = relationship("app.models.plant.Plant", back_populates="plant_state")
