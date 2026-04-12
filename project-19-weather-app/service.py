import requests


class WeatherService:
    """
    Service to fetch weather data
    """

    def __init__(self, api_key=None):
        self.api_key = api_key

    def get_weather_data(self, city):
        """
        Fetch weather data for a specific city using Open-Meteo APIs.
        """

        # Step 1: Convert city → latitude & longitude
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}

        geo_response = requests.get(geo_url, params=geo_params)
        if not geo_response.ok:
            print("Error fetching geocoding data.")
            return None

        geo_data = geo_response.json()
        results = geo_data.get("results")

        if not results:
            print(f"Error: no geocoding results found for '{city}'.")
            return None

        lat = results[0]["latitude"]
        lng = results[0]["longitude"]

        # Step 2: Fetch weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lng,
            "hourly": "temperature_2m",
            "forecast_days": 1,
        }

        weather_response = requests.get(weather_url, params=weather_params)
        if not weather_response.ok:
            print("Error fetching weather data from Open-Meteo.")
            return None

        weather_data = weather_response.json()

        hourly = weather_data.get("hourly", {})
        temperatures = hourly.get("temperature_2m")
        times = hourly.get("time")

        if not temperatures or not times:
            print("Error: unexpected weather API response format.")
            return None

        print("Weather data fetched successfully!")

        return {
            "current_temperature": temperatures[0],
            "times": times[:24],
            "temperatures": temperatures[:24],
        }
