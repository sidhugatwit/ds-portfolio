"""Weather data from Open-Meteo (free, no API key): geocoding, current conditions and a 24-hour forecast."""
import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 15  # seconds


class WeatherService:
    def __init__(self, session=None):
        self.http = session or requests.Session()

    def geocode(self, city):
        """Best match for a city name: name, country, latitude, longitude. None if not found."""
        r = self.http.get(GEO_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=TIMEOUT)
        r.raise_for_status()
        results = r.json().get("results")
        if not results:
            return None
        top = results[0]
        return {"name": top["name"], "country": top.get("country", ""),
                "latitude": top["latitude"], "longitude": top["longitude"]}

    def get_weather_data(self, city):
        """Current temperature plus the next 24 hourly temperatures, in the city's local time.
        Returns None if the city isn't found."""
        place = self.geocode(city)
        if place is None:
            return None
        r = self.http.get(FORECAST_URL, timeout=TIMEOUT, params={
            "latitude": place["latitude"], "longitude": place["longitude"],
            "current": "temperature_2m", "hourly": "temperature_2m",
            "forecast_days": 2, "timezone": "auto",
        })
        r.raise_for_status()
        data = r.json()
        current = data.get("current", {})
        hourly = data.get("hourly", {})
        times, temps = hourly.get("time") or [], hourly.get("temperature_2m") or []
        if current.get("temperature_2m") is None or not times:
            raise ValueError("Unexpected Open-Meteo response format")
        # Hourly data starts at local midnight today: start from the current hour.
        start = next((i for i, t in enumerate(times) if t >= current.get("time", "")[:13]), 0)
        return {
            "place": f"{place['name']}, {place['country']}".strip(", "),
            "timezone": data.get("timezone_abbreviation") or data.get("timezone", "local"),
            "observed_at": current.get("time"),
            "current_temperature": current["temperature_2m"],
            "times": times[start:start + 24],
            "temperatures": temps[start:start + 24],
        }
