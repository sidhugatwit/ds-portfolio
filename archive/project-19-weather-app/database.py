"""SQLite cache: a city's weather is fetched at most once an hour."""
import json
import os
import sqlite3
from datetime import datetime, timedelta

CACHE_FOR = timedelta(hours=1)


class WeatherDatabase:
    def __init__(self, db_file):
        folder = os.path.dirname(db_file)
        if folder:
            os.makedirs(folder, exist_ok=True)
        self.conn = sqlite3.connect(db_file)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS weather (
                   city TEXT PRIMARY KEY,
                   payload TEXT NOT NULL,
                   fetched_at TEXT NOT NULL
               )"""
        )
        self.conn.commit()

    def reset_database(self):
        self.conn.execute("DELETE FROM weather")
        self.conn.commit()

    def get_weather_data(self, weather_service, city, now=None):
        """Cached data if it's less than an hour old; otherwise fetch, store and return fresh data.
        Adds "cached": True or False so the caller can say which it was."""
        now = now or datetime.now()
        key = city.strip().lower()
        row = self.conn.execute("SELECT payload, fetched_at FROM weather WHERE city = ?", (key,)).fetchone()
        if row and now - datetime.fromisoformat(row[1]) < CACHE_FOR:
            return {**json.loads(row[0]), "cached": True}

        data = weather_service.get_weather_data(city)
        if data is None:
            return None
        self.conn.execute(
            "INSERT OR REPLACE INTO weather (city, payload, fetched_at) VALUES (?, ?, ?)",
            (key, json.dumps(data), now.isoformat()),
        )
        self.conn.commit()
        return {**data, "cached": False}

    def close(self):
        self.conn.close()
