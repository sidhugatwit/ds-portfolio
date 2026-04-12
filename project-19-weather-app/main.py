import argparse

from database import WeatherDatabase
from service import WeatherService
from plotter import plot_temperature

# Global constants
DB_FILE = "data/weather_database.db"
API_KEY = None


def main():
    """
    Main function to run the program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City to get the weather data for")
    parser.add_argument("--reset", action="store_true", help="Reset the database")
    args = parser.parse_args()

    db = WeatherDatabase(DB_FILE)
    service = WeatherService(API_KEY)

    if args.reset:
        db.reset_database()

    city_weather_data = db.get_weather_data(service, args.city)

    if city_weather_data is None:
        print(f"Could not retrieve weather data for {args.city}.")
    else:
        print(
            f"Current temperature in {args.city}: "
            f"{city_weather_data['current_temperature']}°C"
        )

        if city_weather_data["times"] and city_weather_data["temperatures"]:
            plot_temperature(
                args.city, city_weather_data["times"], city_weather_data["temperatures"]
            )


if __name__ == "__main__":
    main()
