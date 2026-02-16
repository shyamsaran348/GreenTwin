from fastapi import APIRouter, HTTPException
from app.services.weather_service import weather_service

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)

@router.get("/")
async def get_weather(lat: float, lon: float):
    data = weather_service.get_current_weather(lat, lon)
    if not data:
        raise HTTPException(status_code=503, detail="Weather service unavailable")
    return data
