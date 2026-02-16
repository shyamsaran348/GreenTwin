from datetime import datetime
from app.models.plant_state import PlantState

class TwinEngine:
    @staticmethod
    def calculate_health_score(state: PlantState) -> float:
        """
        Calculate health score using a Novel Synergistic Stress Model.
        Innovation: Stress factors compound non-linearly.
        Formula: Health = 100 * (1 - WaterStress) * (1 - HeatStress) * (1 - DiseaseRisk^1.5)
        """
        # biological constants
        RESILIENCE_FACTOR = 0.1 # Base resistance
        
        water_stress = max(0.0, min(1.0, state.water_stress))
        heat_stress = max(0.0, min(1.0, state.heat_stress))
        disease_risk = max(0.0, min(1.0, state.disease_risk_index))
        
        # Novelty: Multiplicative Impact (Synergy)
        # If a plant is thirsty (0.5) and sick (0.5), it shouldn't just be -50 health.
        # It should be 100 * 0.5 * 0.5 = 25 health (Severe impact).
        
        # Disease is exponential (1.5 power) because it spreads.
        health_factor = (1 - water_stress) * (1 - heat_stress) * (1 - pow(disease_risk, 1.2))
        
        new_health = 100.0 * health_factor
        
        return max(0.0, new_health)

    @staticmethod
    def update_after_disease_prediction(state: PlantState, confidence: float, disease_class: str) -> PlantState:
        """
        Update twin state based on ML disease prediction.
        """
        # Check if the predicted class indicates healthy status (case-insensitive substring)
        if "healthy" in disease_class.lower():
            # Recovery logic: Significant healing if confirmed healthy
            # This allows users to "fix" a false positive by uploading a good leaf
            # If confidence is high, almost completely clear the disease risk
            if confidence > 0.8:
                state.disease_risk_index = 0.0
            else:
                state.disease_risk_index = max(0.0, state.disease_risk_index - 0.5)
        else:
            # Disease detected
            # Aggressive update, but allow for some doubt?
            # No, if model says 98%, we trust it.
            # But we ensure it doesn't go above 1.0
            new_risk = max(state.disease_risk_index, confidence)
            state.disease_risk_index = min(1.0, new_risk)
        
        return state

    @staticmethod
    def simulate_recovery(state: PlantState, water_added: bool = False) -> PlantState:
        """
        Novelty: Biological Recovery Lag.
        Plants don't bounce back instantly. They recover 10% per iteration.
        """
        if water_added:
            # Reduce stress, but not instantly to 0 if it was severe
            state.water_stress = max(0.0, state.water_stress - 0.5)
            
        # Natural healing if stress is low
        if state.water_stress < 0.2 and state.disease_risk_index < 0.2:
             # Slow regeneration
             state.health_score = min(100.0, state.health_score + 5.0)
             
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

    @staticmethod
    def update_from_environment(state: PlantState, temperature: float) -> PlantState:
        """
        Apply environmental factors to the plant twin.
        """
        # Heat Stress Logic
        # Optimal range: 18-30C
        if temperature > 30.0:
            # Heat stress increases
            excess_heat = temperature - 30.0
            # 0.05 stress per degree over 30
            heat_impact = excess_heat * 0.05
            state.heat_stress = min(1.0, state.heat_stress + heat_impact)
            
            # High heat also causes water loss (Evapotranspiration)
            state.water_stress = min(1.0, state.water_stress + (heat_impact * 0.5))
            
        elif temperature < 10.0:
            # Cold stress (reuse heat_stress variable as 'Temperature Stress')
            excess_cold = 10.0 - temperature
            cold_impact = excess_cold * 0.05
            state.heat_stress = min(1.0, state.heat_stress + cold_impact)
        
        else:
            # Ideal range: Recover from temperature stress
            state.heat_stress = max(0.0, state.heat_stress - 0.1)

        state.health_score = TwinEngine.calculate_health_score(state)
        state.last_updated = datetime.utcnow()
        return state
