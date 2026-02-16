from fastapi import APIRouter
from app.services.care_advisor import care_advisor

router = APIRouter(
    prefix="/advice",
    tags=["Advice"]
)

@router.get("/")
def get_plant_advice(species: str, temperature: float, condition: str = "Clear", humidity: float = 50.0, wind_speed: float = 0.0):
    return care_advisor.get_advice(species, temperature, condition, humidity, wind_speed)
