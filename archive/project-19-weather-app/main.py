"""Command line: python main.py Boston [--save forecast.png] [--reset]"""
import argparse
import sys

import requests

from database import WeatherDatabase
from plotter import plot_temperature
from service import WeatherService

DB_FILE = "data/weather_database.db"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Current temperature and a 24-hour forecast (Open-Meteo)")
    parser.add_argument("city", help="City name, e.g. Boston")
    parser.add_argument("--reset", action="store_true", help="Clear the cache first")
    parser.add_argument("--save", metavar="PNG", help="Save the chart to a file instead of opening a window")
    args = parser.parse_args(argv)

    db = WeatherDatabase(DB_FILE)
    if args.reset:
        db.reset_database()
    try:
        data = db.get_weather_data(WeatherService(), args.city)
    except requests.RequestException as e:
        print(f"Couldn't reach Open-Meteo: {e}")
        return 1
    finally:
        db.close()

    if data is None:
        print(f"No city found for '{args.city}'.")
        return 1
    source = "cached, under an hour old" if data["cached"] else "fresh"
    print(f"{data['place']}: {data['current_temperature']}°C at {data['observed_at']} {data['timezone']} ({source})")
    plot_temperature(data["place"], data["times"], data["temperatures"], data["timezone"], save_to=args.save)
    if args.save:
        print(f"Chart saved to {args.save}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
