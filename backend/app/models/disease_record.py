from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class DiseaseRecord(Base):
    __tablename__ = "disease_records"
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    predicted_class = Column(String)
    confidence = Column(Float)
    image_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    plant = relationship("app.models.plant.Plant", back_populates="disease_records")
