"""Offline tests: Open-Meteo responses are simulated, so nothing goes to the network."""
import sys
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database import WeatherDatabase  # noqa: E402
from plotter import plot_temperature  # noqa: E402
from service import WeatherService  # noqa: E402

HOURS = [f"2026-11-10T{h:02d}:00" for h in range(24)] + [f"2026-11-11T{h:02d}:00" for h in range(24)]


class FakeResponse:
    def __init__(self, payload, ok=True):
        self.payload, self.ok = payload, ok

    def json(self):
        return self.payload

    def raise_for_status(self):
        if not self.ok:
            raise RuntimeError("HTTP error")


class FakeSession:
    def __init__(self, geo_results):
        self.geo_results, self.calls = geo_results, 0

    def get(self, url, params=None, timeout=None):
        assert timeout, "every request needs a timeout"
        self.calls += 1
        if "geocoding" in url:
            return FakeResponse({"results": self.geo_results} if self.geo_results else {})
        assert params["current"] == "temperature_2m" and params["timezone"] == "auto"
        return FakeResponse({
            "timezone": "America/New_York", "timezone_abbreviation": "EST",
            "current": {"time": "2026-11-10T14:15", "temperature_2m": 9.4},
            "hourly": {"time": HOURS, "temperature_2m": [float(i) for i in range(48)]},
        })


BOSTON = [{"name": "Boston", "country": "United States", "latitude": 42.36, "longitude": -71.06}]


def test_current_temperature_comes_from_current_not_midnight():
    data = WeatherService(FakeSession(BOSTON)).get_weather_data("Boston")
    assert data["current_temperature"] == 9.4  # not hourly[0], which is midnight
    assert data["place"] == "Boston, United States" and data["timezone"] == "EST"


def test_forecast_starts_at_current_hour_and_spans_24_hours():
    data = WeatherService(FakeSession(BOSTON)).get_weather_data("Boston")
    assert data["times"][0] == "2026-11-10T14:00" and len(data["times"]) == 24
    assert data["times"][-1] == "2026-11-11T13:00"


def test_unknown_city_returns_none():
    assert WeatherService(FakeSession([])).get_weather_data("Nowhereville") is None


def test_cache_skips_the_api_within_an_hour(tmp_path):
    db = WeatherDatabase(str(tmp_path / "cache" / "w.db"))
    session = FakeSession(BOSTON)
    service = WeatherService(session)
    t0 = datetime(2026, 11, 10, 14, 0)
    first = db.get_weather_data(service, "Boston", now=t0)
    calls = session.calls
    second = db.get_weather_data(service, " boston ", now=t0 + timedelta(minutes=30))
    assert not first["cached"] and second["cached"] and session.calls == calls
    third = db.get_weather_data(service, "Boston", now=t0 + timedelta(minutes=61))
    assert not third["cached"] and session.calls == calls + 2
    db.close()


def test_failed_lookup_is_not_cached(tmp_path):
    db = WeatherDatabase(str(tmp_path / "w.db"))
    assert db.get_weather_data(WeatherService(FakeSession([])), "Nowhereville") is None
    assert db.conn.execute("SELECT COUNT(*) FROM weather").fetchone()[0] == 0
    db.close()


def test_plot_saves_png(tmp_path):
    out = tmp_path / "chart.png"
    plot_temperature("Boston, United States", HOURS[:24], list(range(24)), "EST", save_to=str(out))
    assert out.exists() and out.stat().st_size > 1000


def test_plot_rejects_empty_data():
    with pytest.raises(ValueError):
        plot_temperature("Boston", [], [])
