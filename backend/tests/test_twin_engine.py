import unittest
from app.services.twin_engine import TwinEngine
from app.models.plant_state import PlantState
from datetime import datetime

class TestTwinEngine(unittest.TestCase):
    def setUp(self):
        self.state = PlantState(
            id=1,
            plant_id=1,
            health_score=100.0,
            growth_stage="seedling",
            water_stress=0.0,
            heat_stress=0.0,
            disease_risk_index=0.0,
            last_updated=datetime.utcnow()
        )

    def test_health_calculation_perfect(self):
        score = TwinEngine.calculate_health_score(self.state)
        self.assertEqual(score, 100.0)

    def test_health_calculation_stressed(self):
        self.state.water_stress = 0.5 # 50% stress -> -10 pts
        score = TwinEngine.calculate_health_score(self.state)
        # 100 - (0.5 * 20) = 90
        self.assertEqual(score, 90.0)

    def test_disease_update(self):
        # Disease detected with 80% confidence
        TwinEngine.update_after_disease_prediction(self.state, 0.8, "Late Blight")
        # Risk increases by 0.8 * 0.5 = 0.4
        self.assertEqual(self.state.disease_risk_index, 0.4)
        
        # Health should drop
        # 100 - (0.4 * 50) = 80
        self.assertEqual(self.state.health_score, 80.0)

    def test_recovery(self):
        self.state.disease_risk_index = 0.5
        TwinEngine.update_after_disease_prediction(self.state, 0.9, "Healthy")
        self.assertEqual(self.state.disease_risk_index, 0.4)

if __name__ == '__main__':
    unittest.main()
