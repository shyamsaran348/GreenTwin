from datetime import datetime
from app.models.plant_state import PlantState

class TwinEngine:
    @staticmethod
    def calculate_health_score(state: PlantState) -> float:
        """
        Calculate health score (0-100) based on stress factors and disease risk.
        Formula: Base (100) - (WaterStress * 20) - (HeatStress * 20) - (DiseaseRisk * 50)
        """
        # Ensure values are within bounds
        water_stress = max(0.0, min(1.0, state.water_stress))
        heat_stress = max(0.0, min(1.0, state.heat_stress))
        disease_risk = max(0.0, min(1.0, state.disease_risk_index))
        
        # Simple deductive model
        penalty = (water_stress * 20) + (heat_stress * 20) + (disease_risk * 50)
        
        new_health = 100.0 - penalty
        return max(0.0, new_health)

    @staticmethod
    def update_after_disease_prediction(state: PlantState, confidence: float, disease_class: str) -> PlantState:
        """
        Update twin state based on ML disease prediction.
        """
        if disease_class.lower() == "healthy":
            # Recovery logic: reduce disease risk over time if consistently healthy
            state.disease_risk_index = max(0.0, state.disease_risk_index - 0.1)
        else:
            # Disease detected
            # Increase risk based on confidence
            state.disease_risk_index = min(1.0, state.disease_risk_index + (confidence * 0.5))
        
        state.health_score = TwinEngine.calculate_health_score(state)
        state.last_updated = datetime.utcnow()
        return state

    @staticmethod
    def update_stress(state: PlantState, water_stress_delta: float = 0, heat_stress_delta: float = 0) -> PlantState:
        """
        Update physiological stress factors.
        """
        state.water_stress = max(0.0, min(1.0, state.water_stress + water_stress_delta))
        state.heat_stress = max(0.0, min(1.0, state.heat_stress + heat_stress_delta))
        
        state.health_score = TwinEngine.calculate_health_score(state)
        state.last_updated = datetime.utcnow()
        return state
