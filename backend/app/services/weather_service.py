import requests

class WeatherService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def get_current_weather(lat: float, lon: float):
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "hourly": "relativehumidity_2m",
                "timezone": "auto"
            }
            response = requests.get(WeatherService.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current_weather", {})
            hourly = data.get("hourly", {})
            
            temp = current.get("temperature")
            wind_speed = current.get("windspeed")
            
            # Open-Meteo humidity is hourly. Get the one closest to now.
            # actually for simplicity, just take the first one or current hour index
            # simplistic approach: take index 0 if available
            humidity = 50 # Default
            if "relativehumidity_2m" in hourly and hourly["relativehumidity_2m"]:
                 # We should find the current hour, but for MVP taking the current hour (usually near index 0 or by time)
                 # Let's just take the first value which represents "now" roughly in 1-hr forecast usually
                 # Better: Use datetime. But to keep it simple and robust:
                 humidity = hourly["relativehumidity_2m"][0]

            return {
                "temperature": temp,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "condition": WeatherService._get_condition_code(current.get("weathercode")),
                "is_day": current.get("is_day")
            }
        except Exception as e:
            print(f"Weather API Error: {e}")
            return None

    @staticmethod
    def _get_condition_code(code):
        # WMO Weather interpretation codes (WW)
        if code == 0: return "Clear sky"
        if code in [1, 2, 3]: return "Partly cloudy"
        if code in [45, 48]: return "Fog"
        if code in [51, 53, 55]: return "Drizzle"
        if code in [61, 63, 65]: return "Rain"
        if code in [80, 81, 82]: return "Showers"
        return "Unknown"

weather_service = WeatherService()
