from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from datetime import datetime

from app import database
from app.models.plant import Plant
from app.models.disease_record import DiseaseRecord
from app.models.user import User
from app.dependencies import get_current_user
from app.ml.inference import inference_service
from app.services.twin_engine import TwinEngine

router = APIRouter(
    prefix="/disease",
    tags=["Disease Intelligence"]
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/analyze/{plant_id}")
async def analyze_leaf(
    plant_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db), 
    current_user: User = Depends(get_current_user)
):
    # Verify plant ownership
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    # Save file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(UPLOAD_DIR, f"{plant_id}_{timestamp}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Run Inference
    result = inference_service.predict(file_path)
    predicted_class = result["class"]
    confidence = result["confidence"]
    
    # Update Digital Twin
    if plant.plant_state:
        updated_state = TwinEngine.update_after_disease_prediction(
            plant.plant_state, 
            confidence if predicted_class != "Healthy" else 0.0, # Pass confidence logic adjustment
            predicted_class
        )
        # Recalculate health score explicitly to ensure it updates
        updated_state.health_score = TwinEngine.calculate_health_score(updated_state)
        db.add(updated_state)
    
    # Record History
    record = DiseaseRecord(
        plant_id=plant_id,
        predicted_class=predicted_class,
        confidence=confidence,
        image_path=file_path
    )
    db.add(record)
    db.commit()
    
    return {
        "plant_id": plant_id,
        "disease": predicted_class,
        "confidence": confidence,
        "health_score": plant.plant_state.health_score if plant.plant_state else None,
        "image_path": file_path
    }
