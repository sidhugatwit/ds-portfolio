import os
import sqlite3
from datetime import datetime, timedelta


class WeatherDatabase:
    """
    Database class to interact with the weather database.
    """

    def __init__(self, db_file):
        # Ensure data folder exists
        os.makedirs("data", exist_ok=True)

        # Initialize connection safely
        self.conn = None
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temperature REAL,
                timestamp TEXT
            )
        """
        )
        self.conn.commit()

    def reset_database(self):
        self.cursor.execute("DELETE FROM weather")
        self.conn.commit()
        print("Database deleted!")

    def get_weather_data(self, weather_service, city):
        """
        Retrieve weather data for a specific city.
        Uses cached current temperature if it is less than 1 hour old,
        but still fetches fresh forecast data for plotting.
        """
        self.cursor.execute(
            """
            SELECT temperature, timestamp
            FROM weather
            WHERE city = ?
            ORDER BY id DESC
            LIMIT 1
        """,
            (city,),
        )
        data = self.cursor.fetchone()

        weather_data = weather_service.get_weather_data(city)
        if weather_data is None:
            return None

        if data:
            temperature, timestamp = data
            if timestamp:
                saved_time = datetime.fromisoformat(timestamp)
                if datetime.now() - saved_time < timedelta(hours=1):
                    print("Using cached weather data.")
                    weather_data["current_temperature"] = temperature
                    return weather_data

        now = datetime.now().isoformat()

        self.cursor.execute(
            """
            INSERT INTO weather (city, temperature, timestamp)
            VALUES (?, ?, ?)
        """,
            (city, weather_data["current_temperature"], now),
        )

        self.conn.commit()
        return weather_data

    def __del__(self):
        # Safe cleanup
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
